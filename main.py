"""
IBEX Coin Bot - Ana Dosya
Built to Climb 🐐

Calistirmak icin: python main.py
(Once .env dosyasini olusturup BOT_TOKEN vs. bilgilerini girmeyi unutmayin)
"""
import logging
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

import config
import database as db
from handlers import captcha, moderation, admin, info_commands, airdrop, giveaway, xp, language, general

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("ibex_bot")


async def post_init(application: Application):
    await db.init_db()
    logger.info("Veritabani hazir.")
    bot_info = await application.bot.get_me()
    logger.info("IBEX Bot baslatildi: @%s", bot_info.username)


def build_application() -> Application:
    app = ApplicationBuilder().token(config.BOT_TOKEN).post_init(post_init).build()

    # --- Genel komutlar ---
    app.add_handler(CommandHandler("start", general.start_command))
    app.add_handler(CommandHandler("help", general.help_command))
    app.add_handler(CommandHandler("yardim", general.help_command))

    # --- Dil ---
    app.add_handler(CommandHandler(["dil", "language"], language.language_command))
    app.add_handler(CallbackQueryHandler(language.language_callback, pattern=r"^lang:"))

    # --- Bilgi komutlari ---
    app.add_handler(CommandHandler("price", info_commands.price_command))
    app.add_handler(CommandHandler("chart", info_commands.chart_command))
    app.add_handler(CommandHandler("holders", info_commands.holders_command))
    app.add_handler(CommandHandler("buy", info_commands.buy_command))
    app.add_handler(CommandHandler("website", info_commands.website_command))
    app.add_handler(CommandHandler("twitter", info_commands.twitter_command))
    app.add_handler(CommandHandler("telegram", info_commands.telegram_command))
    app.add_handler(CommandHandler(["istatistik", "stats"], info_commands.stats_command))

    # --- Airdrop (conversation) ---
    app.add_handler(airdrop.build_airdrop_conversation())

    # --- Cekilis ---
    app.add_handler(CommandHandler(["cekilis", "giveaway"], giveaway.giveaway_info))
    app.add_handler(CommandHandler(["katil", "join"], giveaway.giveaway_join))
    app.add_handler(CommandHandler(["cekilisbaslat", "startgiveaway"], giveaway.giveaway_start))
    app.add_handler(CommandHandler(["cekilisbitir", "endgiveaway"], giveaway.giveaway_end))

    # --- XP / Seviye ---
    app.add_handler(CommandHandler(["seviye", "level"], xp.my_level))
    app.add_handler(CommandHandler(["liderlik", "leaderboard"], xp.leaderboard))

    # --- Admin paneli ve moderasyon komutlari ---
    app.add_handler(CommandHandler("admin", admin.admin_panel))
    app.add_handler(CallbackQueryHandler(admin.admin_panel_callback, pattern=r"^admin:"))
    app.add_handler(CommandHandler(["duyuru", "announce"], admin.announce))
    app.add_handler(CommandHandler("ban", admin.ban_user))
    app.add_handler(CommandHandler("unban", admin.unban_user))
    app.add_handler(CommandHandler("mute", admin.mute_user))
    app.add_handler(CommandHandler("unmute", admin.unmute_user))

    # --- Captcha (yeni uye dogrulama) ---
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, captcha.on_new_member))
    app.add_handler(CallbackQueryHandler(captcha.on_captcha_click, pattern=r"^captcha:"))

    # --- Moderasyon (spam/scam/reklam + XP kazanma) ---
    # Not: bu handler grup=1 ile en son calisir, boylece komutlar once islenir.
    app.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, moderation.on_group_message),
        group=1,
    )

    return app


def main():
    app = build_application()
    logger.info("IBEX Coin Bot calisiyor... (Built to Climb 🐐)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
