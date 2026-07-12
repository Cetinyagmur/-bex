"""
IBEX Coin Bot - Konfigurasyon Modulu
Tum ayarlar .env dosyasindan okunur.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _get_bool(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def _get_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


BOT_TOKEN = os.getenv("BOT_TOKEN", "")

ADMIN_IDS = set()
_admin_raw = os.getenv("ADMIN_IDS", "")
for _piece in _admin_raw.split(","):
    _piece = _piece.strip()
    if _piece.isdigit():
        ADMIN_IDS.add(int(_piece))

TOKEN_NAME = os.getenv("TOKEN_NAME", "Ibex Coin")
TOKEN_SYMBOL = os.getenv("TOKEN_SYMBOL", "IBEX")
CHAIN = os.getenv("CHAIN", "solana")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "")
DEXSCREENER_PAIR_ADDRESS = os.getenv("DEXSCREENER_PAIR_ADDRESS", "")

WEBSITE_URL = os.getenv("WEBSITE_URL", "")
TWITTER_URL = os.getenv("TWITTER_URL", "")
TELEGRAM_URL = os.getenv("TELEGRAM_URL", "")
BUY_URL = os.getenv("BUY_URL", "")

SOLSCAN_API_KEY = os.getenv("SOLSCAN_API_KEY", "")

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "tr")
CAPTCHA_TIMEOUT = _get_int("CAPTCHA_TIMEOUT", 120)
XP_COOLDOWN = _get_int("XP_COOLDOWN", 60)
XP_PER_MESSAGE = _get_int("XP_PER_MESSAGE", 5)

DB_PATH = os.getenv("DB_PATH", "ibex_bot.db")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN bulunamadi! Lutfen .env dosyanizda BOT_TOKEN degiskenini tanimlayin."
    )
