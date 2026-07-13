"""
IBEX Coin Bot - Veritabani Modulu
SQLite kullanir (aiosqlite). Railway'de dosya kalici degildir; kalici veri
istiyorsaniz Railway'in "Volume" ozelligini ekleyip DB_PATH'i o volume'e
yonlendirin (README'de anlatildi).
"""
import time
import aiosqlite
import config

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    lang TEXT DEFAULT 'tr',
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    last_xp_time INTEGER DEFAULT 0,
    joined_at INTEGER,
    is_banned INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS captcha_pending (
    user_id INTEGER,
    chat_id INTEGER,
    correct_answer INTEGER,
    message_id INTEGER,
    join_time INTEGER,
    PRIMARY KEY (user_id, chat_id)
);

CREATE TABLE IF NOT EXISTS warnings (
    user_id INTEGER,
    chat_id INTEGER,
    count INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, chat_id)
);

CREATE TABLE IF NOT EXISTS airdrop_entries (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    wallet TEXT,
    submitted_at INTEGER
);

CREATE TABLE IF NOT EXISTS giveaways (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prize TEXT,
    is_active INTEGER DEFAULT 1,
    winner_id INTEGER,
    created_at INTEGER
);

CREATE TABLE IF NOT EXISTS giveaway_entries (
    giveaway_id INTEGER,
    user_id INTEGER,
    username TEXT,
    PRIMARY KEY (giveaway_id, user_id)
);
"""


async def init_db():
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.executescript(_SCHEMA)
        await db.commit()


async def get_or_create_user(user_id: int, username: str, first_name: str):
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        if row:
            await db.execute(
                "UPDATE users SET username = ?, first_name = ? WHERE user_id = ?",
                (username, first_name, user_id),
            )
            await db.commit()
            return dict(row)
        await db.execute(
            "INSERT INTO users (user_id, username, first_name, lang, joined_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, first_name, config.DEFAULT_LANGUAGE, int(time.time())),
        )
        await db.commit()
        cur = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        return dict(row)


async def set_user_lang(user_id: int, lang: str):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
        await db.commit()


async def get_user_lang(user_id: int) -> str:
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else config.DEFAULT_LANGUAGE


async def add_captcha(user_id, chat_id, correct_answer, message_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO captcha_pending "
            "(user_id, chat_id, correct_answer, message_id, join_time) VALUES (?, ?, ?, ?, ?)",
            (user_id, chat_id, correct_answer, message_id, int(time.time())),
        )
        await db.commit()


async def get_captcha(user_id, chat_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM captcha_pending WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id),
        )
        row = await cur.fetchone()
        return dict(row) if row else None


async def remove_captcha(user_id, chat_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "DELETE FROM captcha_pending WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id),
        )
        await db.commit()


async def add_warning(user_id, chat_id) -> int:
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT count FROM warnings WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)
        )
        row = await cur.fetchone()
        new_count = (row["count"] if row else 0) + 1
        await db.execute(
            "INSERT OR REPLACE INTO warnings (user_id, chat_id, count) VALUES (?, ?, ?)",
            (user_id, chat_id, new_count),
        )
        await db.commit()
        return new_count


async def add_xp(user_id: int, amount: int):
    """XP ekler, cooldown kontrolu yapar, seviye atlama olup olmadigini dondurur."""
    now = int(time.time())
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT xp, level, last_xp_time FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cur.fetchone()
        if not row:
            return None
        if now - row["last_xp_time"] < config.XP_COOLDOWN:
            return None  # cooldown aktif, XP verilmez

        new_xp = row["xp"] + amount
        old_level = row["level"]
        # basit seviye formulu: her seviye icin (level * 100) XP gerekir
        new_level = old_level
        remaining = new_xp
        threshold = new_level * 100
        while remaining >= threshold:
            new_level += 1
            threshold = new_level * 100

        await db.execute(
            "UPDATE users SET xp = ?, level = ?, last_xp_time = ? WHERE user_id = ?",
            (new_xp, new_level, now, user_id),
        )
        await db.commit()
        return {"leveled_up": new_level > old_level, "new_level": new_level, "xp": new_xp}


async def get_leaderboard(limit: int = 10):
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT username, first_name, xp, level FROM users ORDER BY xp DESC LIMIT ?",
            (limit,),
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def get_stats():
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        total_users = (await cur.fetchone())[0]
        cur = await db.execute("SELECT COUNT(*) FROM airdrop_entries")
        total_airdrop = (await cur.fetchone())[0]
        cur = await db.execute("SELECT COUNT(*) FROM giveaways WHERE is_active = 1")
        active_giveaways = (await cur.fetchone())[0]
        return {
            "total_users": total_users,
            "total_airdrop": total_airdrop,
            "active_giveaways": active_giveaways,
        }


async def add_airdrop_entry(user_id, username, wallet):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO airdrop_entries (user_id, username, wallet, submitted_at) "
            "VALUES (?, ?, ?, ?)",
            (user_id, username, wallet, int(time.time())),
        )
        await db.commit()


async def has_airdrop_entry(user_id) -> bool:
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("SELECT 1 FROM airdrop_entries WHERE user_id = ?", (user_id,))
        return (await cur.fetchone()) is not None


async def get_all_airdrop_entries():
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM airdrop_entries ORDER BY submitted_at ASC")
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def create_giveaway(prize: str) -> int:
    async with aiosqlite.connect(config.DB_PATH) as db:
        # onceki aktif cekilisleri kapat
        await db.execute("UPDATE giveaways SET is_active = 0 WHERE is_active = 1")
        cur = await db.execute(
            "INSERT INTO giveaways (prize, is_active, created_at) VALUES (?, 1, ?)",
            (prize, int(time.time())),
        )
        await db.commit()
        return cur.lastrowid


async def get_active_giveaway():
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM giveaways WHERE is_active = 1 LIMIT 1")
        row = await cur.fetchone()
        return dict(row) if row else None


async def join_giveaway(giveaway_id, user_id, username) -> bool:
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute(
            "SELECT 1 FROM giveaway_entries WHERE giveaway_id = ? AND user_id = ?",
            (giveaway_id, user_id),
        )
        if await cur.fetchone():
            return False
        await db.execute(
            "INSERT INTO giveaway_entries (giveaway_id, user_id, username) VALUES (?, ?, ?)",
            (giveaway_id, user_id, username),
        )
        await db.commit()
        return True


async def get_giveaway_entries(giveaway_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM giveaway_entries WHERE giveaway_id = ?", (giveaway_id,)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def close_giveaway(giveaway_id, winner_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "UPDATE giveaways SET is_active = 0, winner_id = ? WHERE id = ?",
            (winner_id, giveaway_id),
        )
        await db.commit()


async def set_ban(user_id: int, banned: bool):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "UPDATE users SET is_banned = ? WHERE user_id = ?", (1 if banned else 0, user_id)
        )
        await db.commit()


async def get_all_user_ids():
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("SELECT user_id FROM users")
        rows = await cur.fetchall()
        return [r[0] for r in rows]
