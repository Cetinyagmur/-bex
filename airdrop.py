"""
IBEX Coin Bot - Airdrop Yonetimi
Kullanici /airdrop yazar -> cuzdan adresi ister -> kullanici cuzdanini
mesaj olarak gonderir -> conversation state ile yakalanip kaydedilir.
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler

import database as db
import utils
from i18n import t

WAITING_WALLET = 1


async def airdrop_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]

    if await db.has_airdrop_entry(user.id):
        await update.message.reply_text(t("airdrop_already", lang))
        return ConversationHandler.END

    await update.message.reply_text(t("airdrop_intro", lang), parse_mode="Markdown")
    return WAITING_WALLET


async def airdrop_receive_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    wallet = update.message.text.strip()

    if not utils.is_valid_solana_address(wallet):
        await update.message.reply_text(t("airdrop_invalid_wallet", lang))
        return WAITING_WALLET

    await db.add_airdrop_entry(user.id, user.username or "", wallet)
    await update.message.reply_text(t("airdrop_registered", lang, wallet=wallet), parse_mode="Markdown")
    return ConversationHandler.END


async def airdrop_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("İptal edildi." )
    return ConversationHandler.END


def build_airdrop_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler(["airdrop"], airdrop_start)],
        states={
            WAITING_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, airdrop_receive_wallet)],
        },
        fallbacks=[CommandHandler("iptal", airdrop_cancel), CommandHandler("cancel", airdrop_cancel)],
        conversation_timeout=300,
    )
