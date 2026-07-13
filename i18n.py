"""
IBEX Coin Bot - Turkce / Ingilizce metin sozlugu
"""
import config

TEXTS = {
    "welcome_caption": {
        "tr": (
            "🏔️ *{token_name} ({symbol})* topluluğuna hoş geldin, {mention}!\n\n"
            "*Built to Climb* 🐐\n\n"
            "Devam edebilmek için aşağıdaki doğrulamayı tamamla.\n"
            "⏳ Süre: {timeout} saniye"
        ),
        "en": (
            "🏔️ Welcome to *{token_name} ({symbol})*, {mention}!\n\n"
            "*Built to Climb* 🐐\n\n"
            "Please complete the verification below to continue.\n"
            "⏳ Time limit: {timeout} seconds"
        ),
    },
    "captcha_question": {
        "tr": "🧮 Doğrulama: *{a} + {b} = ?*\nDoğru cevabı aşağıdan seç.",
        "en": "🧮 Verification: *{a} + {b} = ?*\nPick the correct answer below.",
    },
    "captcha_success": {
        "tr": "✅ Doğrulama başarılı! Aramıza hoş geldin {mention} 🎉",
        "en": "✅ Verification successful! Welcome {mention} 🎉",
    },
    "captcha_fail": {
        "tr": "❌ Yanlış cevap, tekrar dene.",
        "en": "❌ Wrong answer, try again.",
    },
    "captcha_timeout_kick": {
        "tr": "⏰ {mention} doğrulama süresini geçirdiği için gruptan çıkarıldı.",
        "en": "⏰ {mention} was removed for not completing verification in time.",
    },
    "not_your_captcha": {
        "tr": "Bu doğrulama sana ait değil.",
        "en": "This verification is not for you.",
    },
    "spam_deleted": {
        "tr": "🚫 {mention} adlı kullanıcının mesajı spam/reklam olarak algılandığı için silindi.",
        "en": "🚫 A message from {mention} was removed as spam/advertising.",
    },
    "warn_notice": {
        "tr": "⚠️ {mention}, kural ihlali ({count}/3). 3 uyarıda otomatik susturma uygulanır.",
        "en": "⚠️ {mention}, rule violation ({count}/3). Auto-mute applies at 3 warnings.",
    },
    "muted_notice": {
        "tr": "🔇 {mention} 3 uyarı sınırına ulaştığı için 1 saat susturuldu.",
        "en": "🔇 {mention} has been muted for 1 hour after reaching 3 warnings.",
    },
    "admin_only": {
        "tr": "⛔ Bu komutu yalnızca yöneticiler kullanabilir.",
        "en": "⛔ This command is admin-only.",
    },
    "admin_panel_title": {
        "tr": "⚙️ *IBEX Bot Yönetim Paneli*\nAşağıdan bir işlem seç:",
        "en": "⚙️ *IBEX Bot Admin Panel*\nChoose an action below:",
    },
    "announce_usage": {
        "tr": "Kullanım: `/duyuru <mesaj>`",
        "en": "Usage: `/announce <message>`",
    },
    "announce_sent": {
        "tr": "📢 Duyuru {count} kullanıcıya gönderildi.",
        "en": "📢 Announcement sent to {count} users.",
    },
    "price_error": {
        "tr": "⚠️ Fiyat bilgisi alınamadı. Contract adresi doğru mu kontrol et.",
        "en": "⚠️ Could not fetch price data. Check that the contract address is correct.",
    },
    "price_template": {
        "tr": (
            "💰 *{symbol} Fiyat Bilgisi*\n\n"
            "💵 Fiyat: `${price}`\n"
            "📈 24s Değişim: {change_24h}%\n"
            "💧 Likidite: ${liquidity}\n"
            "📊 24s Hacim: ${volume}\n"
            "🏦 Piyasa Değeri: ${mcap}\n\n"
            "[DexScreener'da Aç]({url})"
        ),
        "en": (
            "💰 *{symbol} Price Info*\n\n"
            "💵 Price: `${price}`\n"
            "📈 24h Change: {change_24h}%\n"
            "💧 Liquidity: ${liquidity}\n"
            "📊 24h Volume: ${volume}\n"
            "🏦 Market Cap: ${mcap}\n\n"
            "[Open on DexScreener]({url})"
        ),
    },
    "chart_caption": {
        "tr": "📈 *{symbol}* canlı grafiği için aşağıdaki bağlantıya tıkla:\n{url}",
        "en": "📈 Tap below for the live *{symbol}* chart:\n{url}",
    },
    "holders_no_key": {
        "tr": (
            "👥 Holder sayısı için Solscan API anahtarı tanımlı değil.\n"
            "Zinciri doğrudan görüntülemek için: {explorer_url}"
        ),
        "en": (
            "👥 No Solscan API key configured for holder count.\n"
            "View directly on-chain: {explorer_url}"
        ),
    },
    "holders_template": {
        "tr": "👥 *{symbol}* şu anda *{count}* cüzdan tarafından tutuluyor.",
        "en": "👥 *{symbol}* is currently held by *{count}* wallets.",
    },
    "buy_template": {
        "tr": (
            "💵 *{symbol} Nasıl Alınır*\n\n"
            "1️⃣ Phantom / Solflare gibi bir Solana cüzdanı kur\n"
            "2️⃣ Cüzdanına SOL yükle\n"
            "3️⃣ Aşağıdaki bağlantıdan takas yap\n\n"
            "[Hemen Satın Al]({buy_url})\n\n"
            "Contract: `{contract}`"
        ),
        "en": (
            "💵 *How to Buy {symbol}*\n\n"
            "1️⃣ Set up a Solana wallet (Phantom / Solflare)\n"
            "2️⃣ Fund it with SOL\n"
            "3️⃣ Swap using the link below\n\n"
            "[Buy Now]({buy_url})\n\n"
            "Contract: `{contract}`"
        ),
    },
    "website_template": {"tr": "🌐 Web sitemiz:\n{url}", "en": "🌐 Our website:\n{url}"},
    "twitter_template": {"tr": "🐦 Twitter / X hesabımız:\n{url}", "en": "🐦 Our Twitter / X:\n{url}"},
    "telegram_template": {"tr": "💬 Telegram kanalımız:\n{url}", "en": "💬 Our Telegram channel:\n{url}"},
    "airdrop_intro": {
        "tr": (
            "🎁 *IBEX Airdrop*\n\n"
            "Katılmak için Solana cüzdan adresini gönder.\n"
            "Örnek format: `4Nd1m...cüzdan_adresi`\n\n"
            "Cüzdanını mesaj olarak yaz."
        ),
        "en": (
            "🎁 *IBEX Airdrop*\n\n"
            "Send your Solana wallet address to join.\n"
            "Example format: `4Nd1m...wallet_address`\n\n"
            "Reply with your wallet as a message."
        ),
    },
    "airdrop_already": {
        "tr": "✅ Zaten airdrop listesine kayıtlısın.",
        "en": "✅ You're already registered for the airdrop.",
    },
    "airdrop_invalid_wallet": {
        "tr": "❌ Geçersiz cüzdan formatı. Lütfen geçerli bir Solana adresi gönder.",
        "en": "❌ Invalid wallet format. Please send a valid Solana address.",
    },
    "airdrop_registered": {
        "tr": "✅ Airdrop listesine eklendin! Cüzdan: `{wallet}`",
        "en": "✅ You've been added to the airdrop list! Wallet: `{wallet}`",
    },
    "giveaway_none": {
        "tr": "🎲 Şu anda aktif bir çekiliş yok.",
        "en": "🎲 There is no active giveaway right now.",
    },
    "giveaway_info": {
        "tr": "🎲 *Aktif Çekiliş*\n🏆 Ödül: {prize}\n👥 Katılımcı: {count}\n\nKatılmak için: /katil",
        "en": "🎲 *Active Giveaway*\n🏆 Prize: {prize}\n👥 Entries: {count}\n\nTo join: /join",
    },
    "giveaway_joined": {
        "tr": "🎉 Çekilişe başarıyla katıldın! Bol şans 🍀",
        "en": "🎉 You've successfully joined the giveaway! Good luck 🍀",
    },
    "giveaway_already_joined": {
        "tr": "Zaten bu çekilişe katıldın.",
        "en": "You've already joined this giveaway.",
    },
    "giveaway_created": {
        "tr": "🎲 Yeni çekiliş oluşturuldu!\n🏆 Ödül: {prize}\nKatılmak için: /katil",
        "en": "🎲 New giveaway created!\n🏆 Prize: {prize}\nTo join: /join",
    },
    "giveaway_ended_no_entries": {
        "tr": "Çekilişte katılımcı olmadığı için kazanan seçilemedi.",
        "en": "No entries in the giveaway, so no winner could be selected.",
    },
    "giveaway_winner": {
        "tr": "🏆 Tebrikler {mention}! *{prize}* ödülünü kazandın! 🎉",
        "en": "🏆 Congratulations {mention}! You won *{prize}*! 🎉",
    },
    "xp_level_up": {
        "tr": "🎉 Tebrikler {mention}! Seviye *{level}*'e ulaştın! ⭐",
        "en": "🎉 Congrats {mention}! You reached level *{level}*! ⭐",
    },
    "xp_profile": {
        "tr": "⭐ *{name}*\n🔢 Seviye: {level}\n✨ XP: {xp}",
        "en": "⭐ *{name}*\n🔢 Level: {level}\n✨ XP: {xp}",
    },
    "leaderboard_title": {
        "tr": "🏆 *IBEX Topluluk Liderlik Tablosu*\n\n",
        "en": "🏆 *IBEX Community Leaderboard*\n\n",
    },
    "stats_template": {
        "tr": (
            "📊 *IBEX Bot İstatistikleri*\n\n"
            "👥 Toplam kullanıcı: {total_users}\n"
            "🎁 Airdrop katılımcısı: {total_airdrop}\n"
            "🎲 Aktif çekiliş: {active_giveaways}"
        ),
        "en": (
            "📊 *IBEX Bot Statistics*\n\n"
            "👥 Total users: {total_users}\n"
            "🎁 Airdrop entries: {total_airdrop}\n"
            "🎲 Active giveaways: {active_giveaways}"
        ),
    },
    "lang_changed": {
        "tr": "🌍 Dil Türkçe olarak ayarlandı.",
        "en": "🌍 Language set to English.",
    },
    "choose_language": {
        "tr": "🌍 Lütfen bir dil seç:",
        "en": "🌍 Please choose a language:",
    },
    "start_message": {
        "tr": (
            "🏔️ *{token_name} ({symbol})* botuna hoş geldin!\n\n"
            "*Built to Climb* 🐐\n\n"
            "Kullanılabilir komutlar için /help yaz."
        ),
        "en": (
            "🏔️ Welcome to the *{token_name} ({symbol})* bot!\n\n"
            "*Built to Climb* 🐐\n\n"
            "Type /help to see available commands."
        ),
    },
    "help_message": {
        "tr": (
            "📖 *Komut Listesi*\n\n"
            "💰 /price - Canlı fiyat\n"
            "📈 /chart - Grafik bağlantısı\n"
            "👥 /holders - Holder sayısı\n"
            "💵 /buy - Nasıl satın alınır\n"
            "🌐 /website - Web sitesi\n"
            "🐦 /twitter - Twitter/X\n"
            "💬 /telegram - Telegram kanalı\n"
            "🎁 /airdrop - Airdrop'a katıl\n"
            "🎲 /cekilis - Aktif çekilişi gör\n"
            "🎯 /katil - Çekilişe katıl\n"
            "⭐ /seviye - XP ve seviyeni gör\n"
            "🏆 /liderlik - Liderlik tablosu\n"
            "📊 /istatistik - Bot istatistikleri\n"
            "🌍 /dil - Dil değiştir\n\n"
            "*Yönetici Komutları:*\n"
            "⚙️ /admin - Yönetim paneli\n"
            "📢 /duyuru <mesaj> - Duyuru gönder\n"
            "🎲 /cekilisbaslat <ödül> - Yeni çekiliş\n"
            "🏆 /cekilisbitir - Çekilişi sonlandır\n"
            "🔨 /ban /unban /mute /unmute (reply ile)"
        ),
        "en": (
            "📖 *Command List*\n\n"
            "💰 /price - Live price\n"
            "📈 /chart - Chart link\n"
            "👥 /holders - Holder count\n"
            "💵 /buy - How to buy\n"
            "🌐 /website - Website\n"
            "🐦 /twitter - Twitter/X\n"
            "💬 /telegram - Telegram channel\n"
            "🎁 /airdrop - Join airdrop\n"
            "🎲 /giveaway - View active giveaway\n"
            "🎯 /join - Join giveaway\n"
            "⭐ /level - See your XP and level\n"
            "🏆 /leaderboard - Leaderboard\n"
            "📊 /stats - Bot statistics\n"
            "🌍 /language - Change language\n\n"
            "*Admin Commands:*\n"
            "⚙️ /admin - Admin panel\n"
            "📢 /announce <message> - Send announcement\n"
            "🎲 /startgiveaway <prize> - New giveaway\n"
            "🏆 /endgiveaway - End giveaway\n"
            "🔨 /ban /unban /mute /unmute (reply-based)"
        ),
    },
}


def t(key: str, lang: str = None, **kwargs) -> str:
    lang = lang or config.DEFAULT_LANGUAGE
    entry = TEXTS.get(key)
    if not entry:
        return key
    text = entry.get(lang, entry.get("tr", key))
    try:
        return text.format(**kwargs)
    except Exception:
        return text
