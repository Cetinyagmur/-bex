"""
IBEX Coin Bot - Genel Komutlar
/start /help
"""
from telegram import Update
from telegram.ext import ContextTypes

import config
import database as db
from i18n import t


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    await update.message.reply_text(
        t("start_message", lang, token_name=config.TOKEN_NAME, symbol=config.TOKEN_SYMBOL),
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    await update.message.reply_text(t("help_message", lang), parse_mode="Markdown")
