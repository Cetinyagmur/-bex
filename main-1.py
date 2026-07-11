"""
IBEX Coin Telegram Topluluk Botu
--------------------------------
Özellikler:
1) Yeni üye karşılama + captcha doğrulama (anti-bot)
2) Spam / scam link filtreleme
3) /price komutu (Dexscreener API üzerinden)
4) /duyuru komutu (sadece adminler - tüm gruba duyuru gönderir)

Kurulum: requirements.txt + .env.example dosyalarına bakın.
"""

import os
import re
import random
import logging
import asyncio
from datetime import datetime, timedelta

import httpx
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ChatPermissions,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)

# ----------------------------------------------------------------------------
# AYARLAR (ortam değişkenlerinden okunur, bkz. .env.example)
# ----------------------------------------------------------------------------
BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_IDS = {int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip()}
DEXSCREENER_PAIR_ADDRESS = os.environ.get("DEXSCREENER_PAIR_ADDRESS", "")
TOKEN_NAME = os.environ.get("TOKEN_NAME", "IBEX")
VERIFY_TIMEOUT_SECONDS = int(os.environ.get("VERIFY_TIMEOUT_SECONDS", "300"))  # 5 dk

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("mir_bot")

# Bekleyen doğrulamaları tutar: {(chat_id, user_id): {"answer": int, "job": Job}}
pending_verifications: dict[tuple[int, int], dict] = {}

# Basit spam / scam tespiti için kalıplar
LINK_PATTERN = re.compile(r"(https?://|t\.me/|telegram\.me/|www\.)", re.IGNORECASE)
SCAM_KEYWORDS = [
    "airdrop claim", "free giveaway", "connect wallet now", "seed phrase",
    "private key", "double your", "guaranteed profit", "dm me to invest",
    "customer support", "wallet recovery",
]


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ----------------------------------------------------------------------------
# 1) YENİ ÜYE KARŞILAMA + CAPTCHA DOĞRULAMA
# ----------------------------------------------------------------------------
async def on_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        user_id = member.id

        # Kullanıcıyı doğrulanana kadar mesaj atamaz şekilde kısıtla
        try:
            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
            )
        except Exception as e:
            logger.warning(f"Kısıtlama başarısız: {e}")

        a, b = random.randint(1, 9), random.randint(1, 9)
        correct_answer = a + b
        # Yanlış şıklar üret
        options = {correct_answer}
        while len(options) < 3:
            options.add(correct_answer + random.choice([-3, -2, -1, 1, 2, 3]))
        options = list(options)
        random.shuffle(options)

        keyboard = [
            [InlineKeyboardButton(str(opt), callback_data=f"verify:{user_id}:{opt}")]
            for opt in options
        ]

        msg = await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"👋 Hoş geldin {member.mention_html()}!\n\n"
                f"MIR topluluğuna katılmadan önce bot olmadığını doğrula:\n"
                f"<b>{a} + {b} = ?</b>\n\n"
                f"⏱ {VERIFY_TIMEOUT_SECONDS // 60} dakika içinde doğrulamazsan gruptan çıkarılacaksın."
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        # Zaman aşımında at
        job = context.job_queue.run_once(
            kick_unverified,
            when=VERIFY_TIMEOUT_SECONDS,
            data={"chat_id": chat_id, "user_id": user_id, "message_id": msg.message_id},
        )

        pending_verifications[(chat_id, user_id)] = {"answer": correct_answer, "job": job}


async def kick_unverified(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    chat_id, user_id, message_id = data["chat_id"], data["user_id"], data["message_id"]

    if (chat_id, user_id) in pending_verifications:
        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            await context.bot.unban_chat_member(chat_id, user_id)  # kick, ban değil
            await context.bot.delete_message(chat_id, message_id)
        except Exception as e:
            logger.warning(f"Atma başarısız: {e}")
        pending_verifications.pop((chat_id, user_id), None)


async def on_verify_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    _, target_user_id, chosen = query.data.split(":")
    target_user_id, chosen = int(target_user_id), int(chosen)
    chat_id = query.message.chat_id
    clicker_id = query.from_user.id

    if clicker_id != target_user_id:
        await query.answer("Bu doğrulama sana ait değil.", show_alert=True)
        return

    key = (chat_id, target_user_id)
    record = pending_verifications.get(key)
    if not record:
        await query.answer("Doğrulama süresi dolmuş.", show_alert=True)
        return

    if chosen == record["answer"]:
        record["job"].schedule_removal()
        pending_verifications.pop(key, None)
        try:
            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=target_user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_add_web_page_previews=True,
                ),
            )
        except Exception as e:
            logger.warning(f"Kısıtlama kaldırma başarısız: {e}")
        await query.edit_message_text(f"✅ {query.from_user.first_name} doğrulandı, hoş geldin!")
    else:
        await query.answer("Yanlış cevap, tekrar dene.", show_alert=True)


# ----------------------------------------------------------------------------
# 2) SPAM / SCAM LINK FİLTRELEME
# ----------------------------------------------------------------------------
async def spam_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return
    user = update.effective_user
    if is_admin(user.id):
        return

    text_lower = message.text.lower()
    has_link = bool(LINK_PATTERN.search(message.text))
    has_scam_keyword = any(kw in text_lower for kw in SCAM_KEYWORDS)

    if has_link or has_scam_keyword:
        try:
            await message.delete()
            warn = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"⚠️ {user.mention_html()}, link/şüpheli içerik paylaşımı bu grupta yasak.",
                parse_mode="HTML",
            )
            # Uyarıyı 15 saniye sonra sil (grubu kirletmesin)
            context.job_queue.run_once(
                lambda ctx: ctx.bot.delete_message(warn.chat_id, warn.message_id),
                when=15,
            )
        except Exception as e:
            logger.warning(f"Spam mesaj silme başarısız: {e}")


# ----------------------------------------------------------------------------
# 3) /price KOMUTU (Dexscreener API)
# ----------------------------------------------------------------------------
async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not DEXSCREENER_PAIR_ADDRESS:
        await update.message.reply_text(
            "⚠️ Henüz bir DEX çift adresi ayarlanmadı. Token lansmanından sonra "
            "Dexscreener'daki pair adresini .env dosyasına ekle."
        )
        return

    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{DEXSCREENER_PAIR_ADDRESS}"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            data = resp.json()
    except Exception as e:
        await update.message.reply_text(f"Fiyat alınamadı: {e}")
        return

    pair = data.get("pair") or (data.get("pairs") or [None])[0]
    if not pair:
        await update.message.reply_text("Fiyat verisi bulunamadı.")
        return

    price_usd = pair.get("priceUsd", "N/A")
    change_24h = pair.get("priceChange", {}).get("h24", "N/A")
    liquidity = pair.get("liquidity", {}).get("usd", "N/A")
    fdv = pair.get("fdv", "N/A")
    dex_url = pair.get("url", "")

    text = (
        f"💰 <b>$IBEX — {TOKEN_NAME} Fiyat Bilgisi</b>\n\n"
        f"Fiyat: ${price_usd}\n"
        f"24s Değişim: {change_24h}%\n"
        f"Likidite: ${liquidity}\n"
        f"FDV: ${fdv}\n\n"
        f"🔗 <a href='{dex_url}'>Dexscreener'da gör</a>"
    )
    await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)


# ----------------------------------------------------------------------------
# 4) /duyuru KOMUTU (sadece admin)
# ----------------------------------------------------------------------------
async def announce_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user.id):
        await update.message.reply_text("🚫 Bu komutu sadece adminler kullanabilir.")
        return

    if not context.args:
        await update.message.reply_text("Kullanım: /duyuru <mesaj>")
        return

    announcement_text = " ".join(context.args)
    text = f"📢 <b>DUYURU</b>\n\n{announcement_text}"

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, parse_mode="HTML"
    )
    try:
        await context.bot.pin_chat_message(update.effective_chat.id, sent.message_id)
    except Exception as e:
        logger.warning(f"Pinleme başarısız (bot admin yetkisi kontrol et): {e}")


# ----------------------------------------------------------------------------
# /start ve /help
# ----------------------------------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🐐 Hoş geldin! Ben {TOKEN_NAME} topluluk botuyum.\n\n"
        "Komutlar:\n"
        "/price - anlık fiyat bilgisi\n"
        "/duyuru <mesaj> - (sadece admin) duyuru yayınla"
    )


def build_app() -> Application:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("duyuru", announce_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_new_member))
    app.add_handler(CallbackQueryHandler(on_verify_click, pattern=r"^verify:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, spam_filter))

    return app


if __name__ == "__main__":
    application = build_app()
    logger.info("IBEX Coin bot başlatılıyor...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
