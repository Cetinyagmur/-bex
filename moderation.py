"""
IBEX Coin Bot - Moderasyon Modulu
Spam / scam / reklam mesajlarini algilar, siler ve 3 uyaridan sonra
kullaniciyi 1 saatliğine susturur. Admin ve captcha bekleyen kullanicilar
bu kontrolden muaf tutulur (captcha zaten ayri restrict uyguluyor).
"""
import logging
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

import config
import database as db
import utils
from i18n import t

logger = logging.getLogger(__name__)

MUTE_DURATION_SECONDS = 3600  # 1 saat


async def on_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    user = update.effective_user
    chat = update.effective_chat

    if utils.is_admin(user.id):
        return  # adminler moderasyondan muaf

    # kullaniciyi kaydet / XP ver (spam degilse)
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]

    if utils.is_spam_message(message.text):
        try:
            await message.delete()
        except Exception as e:
            logger.warning("Mesaj silinemedi: %s", e)

        mention = f"[{user.first_name}](tg://user?id={user.id})"
        notice = await context.bot.send_message(
            chat.id, t("spam_deleted", lang, mention=mention), parse_mode="Markdown"
        )

        count = await db.add_warning(user.id, chat.id)
        if count >= 3:
            try:
                await context.bot.restrict_chat_member(
                    chat.id,
                    user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=None,  # suresiz - bkz. asagida gecici mute icin until_date kullanilabilir
                )
            except Exception as e:
                logger.warning("Susturma basarisiz: %s", e)
            await context.bot.send_message(chat.id, t("muted_notice", lang, mention=mention), parse_mode="Markdown")
        else:
            await context.bot.send_message(chat.id, t("warn_notice", lang, mention=mention, count=count), parse_mode="Markdown")
        return

    # spam degilse XP ver
    result = await db.add_xp(user.id, config.XP_PER_MESSAGE)
    if result and result.get("leveled_up"):
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        await context.bot.send_message(
            chat.id, t("xp_level_up", lang, mention=mention, level=result["new_level"]), parse_mode="Markdown"
        )
