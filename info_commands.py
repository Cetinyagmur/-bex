"""
IBEX Coin Bot - Bilgi Komutlari
/price /chart /holders /buy /website /twitter /telegram /stats
"""
from telegram import Update
from telegram.ext import ContextTypes

import config
import database as db
import utils
from i18n import t


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    pair = await utils.fetch_dexscreener_data()
    if not pair:
        await update.message.reply_text(t("price_error", lang))
        return

    price = pair.get("priceUsd", "0")
    change_24h = pair.get("priceChange", {}).get("h24", 0)
    liquidity = utils.format_number((pair.get("liquidity") or {}).get("usd", 0))
    volume = utils.format_number((pair.get("volume") or {}).get("h24", 0))
    mcap = utils.format_number(pair.get("fdv", 0))
    url = pair.get("url", f"https://dexscreener.com/{config.CHAIN}/{config.CONTRACT_ADDRESS}")

    text = t(
        "price_template", lang, symbol=config.TOKEN_SYMBOL, price=price, change_24h=change_24h,
        liquidity=liquidity, volume=volume, mcap=mcap, url=url,
    )
    await update.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=False)


async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    pair = await utils.fetch_dexscreener_data()
    url = (pair or {}).get("url", f"https://dexscreener.com/{config.CHAIN}/{config.CONTRACT_ADDRESS}")
    await update.message.reply_text(
        t("chart_caption", lang, symbol=config.TOKEN_SYMBOL, url=url), parse_mode="Markdown"
    )


async def holders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    count = await utils.fetch_holder_count()
    if count is None:
        explorer_url = f"https://solscan.io/token/{config.CONTRACT_ADDRESS}"
        await update.message.reply_text(t("holders_no_key", lang, explorer_url=explorer_url))
        return
    await update.message.reply_text(t("holders_template", lang, symbol=config.TOKEN_SYMBOL, count=count), parse_mode="Markdown")


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    lang = db_user["lang"]
    await update.message.reply_text(
        t("buy_template", lang, symbol=config.TOKEN_SYMBOL, buy_url=config.BUY_URL, contract=config.CONTRACT_ADDRESS),
        parse_mode="Markdown",
    )


async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db_user = await db.get_or_create_user(update.effective_user.id, update.effective_user.username or "", update.effective_user.first_name or "")
    lang = db_user["lang"]
    await update.message.reply_text(t("website_template", lang, url=config.WEBSITE_URL))


async def twitter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db_user = await db.get_or_create_user(update.effective_user.id, update.effective_user.username or "", update.effective_user.first_name or "")
    lang = db_user["lang"]
    await update.message.reply_text(t("twitter_template", lang, url=config.TWITTER_URL))


async def telegram_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db_user = await db.get_or_create_user(update.effective_user.id, update.effective_user.username or "", update.effective_user.first_name or "")
    lang = db_user["lang"]
    await update.message.reply_text(t("telegram_template", lang, url=config.TELEGRAM_URL))


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db_user = await db.get_or_create_user(update.effective_user.id, update.effective_user.username or "", update.effective_user.first_name or "")
    lang = db_user["lang"]
    stats = await db.get_stats()
    await update.message.reply_text(t("stats_template", lang, **stats), parse_mode="Markdown")

