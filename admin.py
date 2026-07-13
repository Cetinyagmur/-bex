"""
IBEX Coin Bot - Admin Paneli
Telegram inline buton tabanli bir "panel" + ban/mute/unban/unmute komutlari.
"""
import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from telegram.ext import ContextTypes

import database as db
import utils
from i18n import t


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await update.message.reply_text(t("admin_only", lang))
        return

    keyboard = [
        [InlineKeyboardButton("📊 İstatistikler", callback_data="admin:stats")],
        [InlineKeyboardButton("🎁 Airdrop Listesi", callback_data="admin:airdrop_list")],
        [InlineKeyboardButton("🎲 Çekiliş Katılımcıları", callback_data="admin:giveaway_list")],
        [InlineKeyboardButton("🏆 Liderlik Tablosu", callback_data="admin:leaderboard")],
    ]
    await update.message.reply_text(
        t("admin_panel_title", lang), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def admin_panel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await query.answer(t("admin_only", lang), show_alert=True)
        return

    action = query.data.split(":")[1]
    await query.answer()

    if action == "stats":
        stats = await db.get_stats()
        await query.edit_message_text(t("stats_template", lang, **stats), parse_mode="Markdown")

    elif action == "airdrop_list":
        entries = await db.get_all_airdrop_entries()
        if not entries:
            await query.edit_message_text("Henüz airdrop kaydı yok.")
            return
        lines = [f"• @{e['username'] or e['user_id']} — `{e['wallet']}`" for e in entries[:50]]
        text = f"🎁 *Airdrop Listesi* ({len(entries)} kayıt)\n\n" + "\n".join(lines)
        await query.edit_message_text(text[:4000], parse_mode="Markdown")

    elif action == "giveaway_list":
        giveaway = await db.get_active_giveaway()
        if not giveaway:
            await query.edit_message_text(t("giveaway_none", lang))
            return
        entries = await db.get_giveaway_entries(giveaway["id"])
        lines = [f"• @{e['username'] or e['user_id']}" for e in entries[:50]]
        text = f"🎲 *{giveaway['prize']}* — {len(entries)} katılımcı\n\n" + "\n".join(lines)
        await query.edit_message_text(text[:4000] if lines else text, parse_mode="Markdown")

    elif action == "leaderboard":
        top = await db.get_leaderboard(10)
        lines = [
            f"{i+1}. {u['first_name']} — Lv.{u['level']} ({u['xp']} XP)"
            for i, u in enumerate(top)
        ]
        text = t("leaderboard_title", lang) + "\n".join(lines)
        await query.edit_message_text(text, parse_mode="Markdown")


def _get_target_user(update: Update):
    """Komuta reply yapilan mesajdan hedef kullaniciyi bulur."""
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user
    return None


async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await update.message.reply_text(t("admin_only", lang))
        return
    target = _get_target_user(update)
    if not target:
        await update.message.reply_text("Lütfen banlamak istediğiniz kullanıcının mesajına reply yapın.")
        return
    await context.bot.ban_chat_member(update.effective_chat.id, target.id)
    await db.set_ban(target.id, True)
    await update.message.reply_text(f"🔨 {target.first_name} banlandı.")


async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await update.message.reply_text(t("admin_only", lang))
        return
    if not context.args:
        await update.message.reply_text("Kullanım: /unban <user_id>")
        return
    target_id = int(context.args[0])
    await context.bot.unban_chat_member(update.effective_chat.id, target_id)
    await db.set_ban(target_id, False)
    await update.message.reply_text("✅ Kullanıcının banı kaldırıldı.")


async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await update.message.reply_text(t("admin_only", lang))
        return
    target = _get_target_user(update)
    if not target:
        await update.message.reply_text("Lütfen susturmak istediğiniz kullanıcının mesajına reply yapın.")
        return

    minutes = 60
    if context.args and context.args[0].isdigit():
        minutes = int(context.args[0])

    until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=minutes)
    await context.bot.restrict_chat_member(
        update.effective_chat.id, target.id, permissions=ChatPermissions(can_send_messages=False), until_date=until
    )
    await update.message.reply_text(f"🔇 {target.first_name} {minutes} dakika susturuldu.")


async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await update.message.reply_text(t("admin_only", lang))
        return
    target = _get_target_user(update)
    if not target:
        await update.message.reply_text("Lütfen susturması kaldırılacak kullanıcının mesajına reply yapın.")
        return
    full_perms = ChatPermissions(
        can_send_messages=True, can_send_photos=True, can_send_videos=True,
        can_send_other_messages=True, can_add_web_page_previews=True,
    )
    await context.bot.restrict_chat_member(update.effective_chat.id, target.id, permissions=full_perms)
    await update.message.reply_text(f"🔊 {target.first_name} susturması kaldırıldı.")


async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await update.message.reply_text(t("admin_only", lang))
        return
    if not context.args:
        await update.message.reply_text(t("announce_usage", lang), parse_mode="Markdown")
        return

    message_text = "📢 " + " ".join(context.args)
    user_ids = await db.get_all_user_ids()
    sent = 0
    for uid in user_ids:
        try:
            await context.bot.send_message(uid, message_text)
            sent += 1
        except Exception:
            continue
    await update.message.reply_text(t("announce_sent", lang, count=sent))
