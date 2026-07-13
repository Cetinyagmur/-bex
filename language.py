"""
IBEX Coin Bot - Dil Degistirme (TR / EN)
"""
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

import database as db
from i18n import t


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    keyboard = [
        [
            InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang:tr"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang:en"),
        ]
    ]
    await update.message.reply_text(t("choose_language", lang), reply_markup=InlineKeyboardMarkup(keyboard))


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    new_lang = query.data.split(":")[1]
    await db.set_user_lang(query.from_user.id, new_lang)
    await query.answer()
    await query.edit_message_text(t("lang_changed", new_lang))
