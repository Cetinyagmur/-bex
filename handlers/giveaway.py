"""
IBEX Coin Bot - Cekilis (Giveaway) Sistemi
"""
import random
from telegram import Update
from telegram.ext import ContextTypes

import database as db
import utils
from i18n import t


async def giveaway_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]

    giveaway = await db.get_active_giveaway()
    if not giveaway:
        await update.message.reply_text(t("giveaway_none", lang))
        return

    entries = await db.get_giveaway_entries(giveaway["id"])
    await update.message.reply_text(
        t("giveaway_info", lang, prize=giveaway["prize"], count=len(entries)), parse_mode="Markdown"
    )


async def giveaway_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]

    giveaway = await db.get_active_giveaway()
    if not giveaway:
        await update.message.reply_text(t("giveaway_none", lang))
        return

    joined = await db.join_giveaway(giveaway["id"], user.id, user.username or user.first_name)
    if joined:
        await update.message.reply_text(t("giveaway_joined", lang))
    else:
        await update.message.reply_text(t("giveaway_already_joined", lang))


async def giveaway_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await update.message.reply_text(t("admin_only", lang))
        return
    if not context.args:
        await update.message.reply_text("Kullanım: /cekilisbaslat <ödül açıklaması>")
        return

    prize = " ".join(context.args)
    await db.create_giveaway(prize)
    await update.message.reply_text(t("giveaway_created", lang, prize=prize), parse_mode="Markdown")


async def giveaway_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = await db.get_user_lang(user.id)
    if not utils.is_admin(user.id):
        await update.message.reply_text(t("admin_only", lang))
        return

    giveaway = await db.get_active_giveaway()
    if not giveaway:
        await update.message.reply_text(t("giveaway_none", lang))
        return

    entries = await db.get_giveaway_entries(giveaway["id"])
    if not entries:
        await db.close_giveaway(giveaway["id"], winner_id=0)
        await update.message.reply_text(t("giveaway_ended_no_entries", lang))
        return

    winner = random.choice(entries)
    await db.close_giveaway(giveaway["id"], winner["user_id"])
    mention = f"[{winner['username'] or winner['user_id']}](tg://user?id={winner['user_id']})"
    await update.message.reply_text(
        t("giveaway_winner", lang, mention=mention, prize=giveaway["prize"]), parse_mode="Markdown"
    )
