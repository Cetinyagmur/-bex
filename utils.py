"""
IBEX Coin Bot - Yardimci fonksiyonlar
"""
import re
import random
import aiohttp
import config

DEXSCREENER_TOKEN_URL = "https://api.dexscreener.com/latest/dex/tokens/{address}"
DEXSCREENER_PAIR_URL = "https://api.dexscreener.com/latest/dex/pairs/solana/{pair}"

# Solana adresi genelde base58, 32-44 karakter
SOLANA_ADDRESS_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

# Spam / scam / reklam icin sik gorulen anahtar kelimeler ve desenler
SPAM_PATTERNS = [
    r"(?i)\bair ?drop\b.{0,20}\bclaim\b",
    r"(?i)\bfree\b.{0,15}\b(nft|token|crypto|bnb|eth|sol)\b",
    r"(?i)\bpump\b.{0,15}\bsignal\b",
    r"(?i)\bguarantee(d)?\b.{0,15}\bprofit\b",
    r"(?i)\bDM me\b",
    r"(?i)\bwhatsapp\b.{0,10}\+\d{6,}",
    r"(?i)t\.me/\+", # gizli davet linkleri
    r"(?i)\bcashapp\b|\bpaypal\b.{0,10}\binvest\b",
    r"(?i)\b(binary options|forex signals)\b",
]
URL_RE = re.compile(r"(https?://|www\.|t\.me/|bit\.ly/)", re.IGNORECASE)


def is_spam_message(text: str, allow_links: bool = False) -> bool:
    if not text:
        return False
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text):
            return True
    if not allow_links and URL_RE.search(text):
        return True
    return False


def is_valid_solana_address(address: str) -> bool:
    return bool(SOLANA_ADDRESS_RE.match(address.strip()))


async def fetch_dexscreener_data():
    """Contract adresine gore fiyat/likidite/hacim verisi ceker.
    Birden fazla pair varsa en yuksek likiditeye sahip olani secer."""
    if not config.CONTRACT_ADDRESS:
        return None
    url = DEXSCREENER_TOKEN_URL.format(address=config.CONTRACT_ADDRESS)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except Exception:
        return None

    pairs = data.get("pairs") or []
    if not pairs:
        return None

    if config.DEXSCREENER_PAIR_ADDRESS:
        pairs = [p for p in pairs if p.get("pairAddress") == config.DEXSCREENER_PAIR_ADDRESS] or pairs

    best = max(pairs, key=lambda p: (p.get("liquidity") or {}).get("usd") or 0)
    return best


def format_number(n) -> str:
    try:
        n = float(n)
    except (TypeError, ValueError):
        return "N/A"
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n/1_000:.2f}K"
    return f"{n:.2f}"


async def fetch_holder_count():
    """Solscan Pro API ile holder sayisi ceker (API key gerektirir)."""
    if not config.SOLSCAN_API_KEY or not config.CONTRACT_ADDRESS:
        return None
    url = f"https://pro-api.solscan.io/v2.0/token/holders?address={config.CONTRACT_ADDRESS}&page=1&page_size=1"
    headers = {"token": config.SOLSCAN_API_KEY}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get("data", {}).get("total")
    except Exception:
        return None


def generate_captcha():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    correct = a + b
    options = {correct}
    while len(options) < 4:
        options.add(random.randint(2, 18))
    options = list(options)
    random.shuffle(options)
    return a, b, correct, options


def is_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS
