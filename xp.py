"""
IBEX Coin Bot - XP / Seviye Sistemi Komutlari
XP kazanma islemi handlers/moderation.py icindeki on_group_message icinde yapilir
(spam olmayan her mesajda, cooldown'a tabi). Burada sadece goruntuleme komutlari var.
"""
from telegram import Update
from telegram.ext import ContextTypes

import database as db
from i18n import t


async def my_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    await update.message.reply_text(
        t("xp_profile", lang, name=user.first_name, level=db_user["level"], xp=db_user["xp"]),
        parse_mode="Markdown",
    )


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    top = await db.get_leaderboard(10)
    if not top:
        await update.message.reply_text("Henüz kimse XP kazanmadı.")
        return
    lines = [f"{i+1}. {u['first_name']} — Lv.{u['level']} ({u['xp']} XP)" for i, u in enumerate(top)]
    await update.message.reply_text(t("leaderboard_title", lang) + "\n".join(lines), parse_mode="Markdown")
