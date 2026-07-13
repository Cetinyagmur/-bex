"""
IBEX Coin Bot - Yeni Uye Dogrulama (Captcha)
Yeni katilan uyeler dogru cevabi secene kadar mesaj gonderemez (mute).
Sure dolarsa gruptan atilir.
"""
import asyncio
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from telegram.ext import ContextTypes

import config
import database as db
import utils
from i18n import t

logger = logging.getLogger(__name__)

MUTED_PERMISSIONS = ChatPermissions(can_send_messages=False)
FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_audios=True,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
)


async def on_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        user = await db.get_or_create_user(member.id, member.username or "", member.first_name or "")
        lang = user["lang"]

        try:
            await context.bot.restrict_chat_member(chat.id, member.id, permissions=MUTED_PERMISSIONS)
        except Exception as e:
            logger.warning("Kisitlama basarisiz (yeterli yetki olmayabilir): %s", e)

        a, b, correct, options = utils.generate_captcha()
        mention = f"[{member.first_name}](tg://user?id={member.id})"

        keyboard = [
            [InlineKeyboardButton(str(opt), callback_data=f"captcha:{member.id}:{opt}") for opt in options[:2]],
            [InlineKeyboardButton(str(opt), callback_data=f"captcha:{member.id}:{opt}") for opt in options[2:]],
        ]

        caption = t("welcome_caption", lang, token_name=config.TOKEN_NAME, symbol=config.TOKEN_SYMBOL,
                    mention=mention, timeout=config.CAPTCHA_TIMEOUT)
        caption += "\n\n" + t("captcha_question", lang, a=a, b=b)

        sent = await context.bot.send_message(
            chat.id, caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await db.add_captcha(member.id, chat.id, correct, sent.message_id)

        asyncio.create_task(_schedule_timeout(context, chat.id, member.id, sent.message_id, lang))


async def _schedule_timeout(context, chat_id, user_id, message_id, lang):
    await asyncio.sleep(config.CAPTCHA_TIMEOUT)
    pending = await db.get_captcha(user_id, chat_id)
    if not pending:
        return  # zaten dogrulanmis
    try:
        await context.bot.ban_chat_member(chat_id, user_id)
        await context.bot.unban_chat_member(chat_id, user_id)  # kick, ban degil
        mention = f"[Kullanici](tg://user?id={user_id})"
        await context.bot.send_message(chat_id, t("captcha_timeout_kick", lang, mention=mention), parse_mode="Markdown")
    except Exception as e:
        logger.warning("Zaman asimi sonrasi kick basarisiz: %s", e)
    finally:
        await db.remove_captcha(user_id, chat_id)
        try:
            await context.bot.delete_message(chat_id, message_id)
        except Exception:
            pass


async def on_captcha_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    _, target_user_id, answer = query.data.split(":")
    target_user_id = int(target_user_id)
    answer = int(answer)

    clicker_id = query.from_user.id
    chat_id = query.message.chat_id
    lang = await db.get_user_lang(clicker_id)

    if clicker_id != target_user_id:
        await query.answer(t("not_your_captcha", lang), show_alert=True)
        return

    pending = await db.get_captcha(target_user_id, chat_id)
    if not pending:
        await query.answer()
        return

    if answer == pending["correct_answer"]:
        try:
            await context.bot.restrict_chat_member(chat_id, target_user_id, permissions=FULL_PERMISSIONS)
        except Exception as e:
            logger.warning("Yetki verme basarisiz: %s", e)
        await db.remove_captcha(target_user_id, chat_id)
        mention = f"[{query.from_user.first_name}](tg://user?id={target_user_id})"
        await query.edit_message_text(t("captcha_success", lang, mention=mention), parse_mode="Markdown")
    else:
        await query.answer(t("captcha_fail", lang), show_alert=True)
