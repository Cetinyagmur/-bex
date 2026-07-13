# 🐐 IBEX Coin Bot — Kurulum Rehberi

*Built to Climb 🏔️*

Bu bot; captcha ile üye doğrulama, spam/scam/reklam engelleme, admin paneli,
fiyat/grafik/holder bilgisi, airdrop, çekiliş, XP-seviye sistemi ve TR/EN dil
desteği içeren tam kapsamlı bir Telegram topluluk botudur.

Bu rehber **tamamen telefon üzerinden** kurulum yapabilmen için adım adım
hazırlandı. Bilgisayara ihtiyacın yok.

---

## 📁 Proje Yapısı

```
ibex-bot/
├── main.py                  # Botu başlatan ana dosya
├── config.py                # .env'den ayarları okur
├── database.py               # SQLite veritabanı işlemleri
├── i18n.py                   # Türkçe/İngilizce metinler
├── utils.py                  # DexScreener API, spam tespiti, vs.
├── requirements.txt           # Gerekli Python kütüphaneleri
├── Procfile                   # Railway'e "bunu çalıştır" der
├── .env.example                # Örnek ayar dosyası (kopyalayıp doldur)
└── handlers/
    ├── captcha.py             # Yeni üye doğrulama
    ├── moderation.py           # Spam/scam/reklam engelleme
    ├── admin.py                # Admin paneli + ban/mute
    ├── info_commands.py        # /price /chart /holders /buy vs.
    ├── airdrop.py               # Airdrop kayıt sistemi
    ├── giveaway.py              # Çekiliş sistemi
    ├── xp.py                    # XP/seviye görüntüleme
    ├── language.py              # Dil değiştirme
    └── general.py               # /start /help
```

---

## 1️⃣ ADIM: Telegram Botu Oluştur (BotFather)

1. Telegram'da **@BotFather** hesabını aç.
2. `/newbot` yaz ve gönder.
3. Botuna bir isim ver: örn. `Ibex Coin Bot`
4. Kullanıcı adı ver (sonu `bot` ile bitmeli): örn. `IbexCoinBot`
5. BotFather sana bir **token** verecek, şuna benzer:
   `7123456789:AAHk8sJ3...` — **bu tokeni kaydet, kimseyle paylaşma.**
6. BotFather'a `/setprivacy` yaz, botunu seç, **Disable** seç.
   (Bu, botun gruptaki tüm mesajları görebilmesi için gerekli — spam
   filtresi ve XP sistemi için şart.)
7. `/setjoingroups` → **Enable** (botun gruplara eklenebilmesi için).

---

## 2️⃣ ADIM: Kendi Telegram ID'ni Öğren

1. Telegram'da **@userinfobot**'a git, `/start` yaz.
2. Sana bir ID verecek, örn: `123456789`. Bunu not al — botun admini
   sen olacaksın.

---

## 3️⃣ ADIM: Solana Contract Adresini Hazırla

$IBEX token'ının Solana contract (mint) adresine ihtiyacın olacak.
Henüz token'ı oluşturmadıysan (Pump.fun, Raydium vs. üzerinden),
önce onu tamamla, sonra contract adresini `.env` dosyasına gireceksin.

---

## 4️⃣ ADIM: Dosyaları GitHub'a Yükle (Telefon Üzerinden)

### A) GitHub hesabı oluştur
[github.com](https://github.com) adresine git, hesap oluştur (yoksa).

### B) Yeni repo oluştur
1. GitHub uygulamasını aç ya da tarayıcıdan github.com'a gir.
2. Sağ üstteki **+** butonuna bas → **New repository**.
3. İsim ver: `ibex-coin-bot`
4. **Private** seç (kodların herkese açık olmasın).
5. **Create repository** butonuna bas.

### C) Dosyaları yükle
1. Oluşturduğun reponun içinde **"Add file" → "Upload files"** seçeneğine bas.
2. Bu projedeki tüm dosyaları (main.py, config.py, database.py, i18n.py,
   utils.py, requirements.txt, Procfile, handlers/ klasörü içindeki
   tüm dosyalar) sırayla yükle.
   > 💡 Telefonda klasör yapısını korumak için dosyaları teker teker
   > sürüklemek yerine, GitHub mobil tarayıcısında "upload files" ekranına
   > hepsini aynı anda seçip atabilirsin; GitHub `handlers/xxx.py` gibi
   > yol içeren dosya adlarını klasör olarak algılar.
3. **⚠️ `.env` dosyasını YÜKLEME!** Sadece `.env.example` yüklenmeli.
   Gerçek `.env` dosyasını (bot tokenin gibi gizli bilgileri içerdiği için)
   sadece Railway'e adım 6'da gireceğiz.
4. Alt kısımda "Commit changes" butonuna basarak yüklemeyi tamamla.

---

## 5️⃣ ADIM: Railway Hesabı Aç ve Projeyi Bağla

1. [railway.app](https://railway.app) adresine git, **GitHub ile giriş yap**.
2. **New Project** → **Deploy from GitHub repo** seç.
3. Az önce oluşturduğun `ibex-coin-bot` reposunu seç.
4. Railway otomatik olarak `requirements.txt` dosyasını görüp Python
   projesi olduğunu anlayacak ve `Procfile`'daki komutla (`python main.py`)
   botu başlatacak.

---

## 6️⃣ ADIM: Ortam Değişkenlerini (.env) Railway'de Gir

1. Railway projenin içinde **Variables** (Değişkenler) sekmesine gir.
2. `.env.example` dosyasındaki her satırı buraya tek tek ekle:

| Değişken | Örnek Değer | Açıklama |
|---|---|---|
| `BOT_TOKEN` | `7123456789:AAHk8sJ3...` | BotFather'dan aldığın token |
| `ADMIN_IDS` | `123456789` | Senin Telegram ID'n (birden fazlaysa virgülle ayır) |
| `TOKEN_NAME` | `Ibex Coin` | Token adı |
| `TOKEN_SYMBOL` | `IBEX` | Token sembolü |
| `CHAIN` | `solana` | Zincir adı |
| `CONTRACT_ADDRESS` | `xxxxxxx...` | Solana contract adresin |
| `WEBSITE_URL` | `https://ibexcoin.io` | Web sitesi linki |
| `TWITTER_URL` | `https://twitter.com/ibexcoin` | X/Twitter linki |
| `TELEGRAM_URL` | `https://t.me/ibexcoin` | Telegram kanal linki |
| `BUY_URL` | `https://jup.ag/swap/SOL-IBEX` | Satın alma linki (Jupiter/Raydium) |
| `SOLSCAN_API_KEY` | *(boş bırakabilirsin)* | Holder sayısı için opsiyonel |
| `DEFAULT_LANGUAGE` | `tr` | Varsayılan dil |
| `CAPTCHA_TIMEOUT` | `120` | Doğrulama süresi (saniye) |
| `XP_COOLDOWN` | `60` | XP kazanma bekleme süresi |
| `XP_PER_MESSAGE` | `5` | Mesaj başına XP |

3. Her değişkeni ekledikten sonra Railway otomatik olarak projeyi yeniden
   başlatacak (redeploy).

> 💾 **Kalıcı Veri Notu:** Railway'in dosya sistemi her deploy'da sıfırlanabilir.
> SQLite veritabanının (kullanıcı XP'leri, airdrop kayıtları vs.) kalıcı
> olması için Railway'de projenin **Settings → Volumes** kısmından bir
> Volume oluşturup, `DB_PATH` değişkenini o volume'ün yoluna
> (örn. `/data/ibex_bot.db`) ayarlaman önerilir.

---

## 7️⃣ ADIM: Botu Gruba Ekle ve Yetkilendir

1. Botunu IBEX Telegram grubuna ekle.
2. Grup ayarlarından botu **Admin** yap ve şu yetkileri ver:
   - Mesajları sil
   - Kullanıcıları yasakla (ban)
   - Kullanıcıları kısıtla (restrict/mute)
   - Yeni üyeleri davet et (opsiyonel)
3. Bu yetkiler olmadan captcha, spam silme ve mute komutları çalışmaz.

---

## 8️⃣ ADIM: Test Et

Railway'de **Deployments** sekmesinden logları kontrol et. Şunu görmelisin:
```
IBEX Bot baslatildi: @IbexCoinBot
IBEX Coin Bot calisiyor... (Built to Climb 🐐)
```

Telegram'da botuna `/start` yaz — cevap veriyorsa her şey hazır! 🎉

Gruba yeni bir hesapla katılarak captcha'yı test edebilir, `/price` ile
DexScreener bağlantısını, `/admin` ile panel erişimini kontrol edebilirsin.

---

## 📖 Komut Listesi

### Herkes kullanabilir
| Komut | Açıklama |
|---|---|
| `/start` | Botu başlat |
| `/help` | Komut listesi |
| `/price` | Canlı fiyat (DexScreener) |
| `/chart` | Grafik bağlantısı |
| `/holders` | Holder sayısı |
| `/buy` | Nasıl satın alınır |
| `/website` | Web sitesi |
| `/twitter` | Twitter/X |
| `/telegram` | Telegram kanalı |
| `/airdrop` | Airdrop'a katıl (cüzdan ister) |
| `/cekilis` | Aktif çekilişi gör |
| `/katil` | Çekilişe katıl |
| `/seviye` | XP ve seviyeni gör |
| `/liderlik` | Liderlik tablosu |
| `/istatistik` | Bot istatistikleri |
| `/dil` | Dil değiştir (TR/EN) |

### Sadece Yöneticiler
| Komut | Açıklama |
|---|---|
| `/admin` | Yönetim paneli (buton menü) |
| `/duyuru <mesaj>` | Tüm kullanıcılara duyuru gönder |
| `/cekilisbaslat <ödül>` | Yeni çekiliş başlat |
| `/cekilisbitir` | Çekilişi sonlandır, kazananı seç |
| `/ban` | (Mesaja reply ile) kullanıcıyı banla |
| `/unban <user_id>` | Ban kaldır |
| `/mute <dakika>` | (Mesaja reply ile) sustur |
| `/unmute` | (Mesaja reply ile) susturmayı kaldır |

---

## 🛡️ Spam/Scam/Reklam Filtresi Nasıl Çalışır?

- Bilinen scam kalıpları (ör. "ücretsiz airdrop", "garantili kazanç",
  "DM me", gizli davet linkleri) otomatik silinir.
- Link içeren mesajlar varsayılan olarak spam sayılır (adminler hariç).
  Eğer grubunda linklere izin vermek istersen `utils.py` içindeki
  `is_spam_message` fonksiyonunun `allow_links` parametresini
  `moderation.py` üzerinden `True` yapabilirsin.
- 3 uyarı alan kullanıcı otomatik olarak 1 saat susturulur.

---

## ⭐ XP / Seviye Sistemi Nasıl Çalışır?

- Spam olmayan her mesaj için kullanıcıya XP verilir (varsayılan: 5 XP,
  60 saniyede bir — XP farming'i engellemek için).
- Seviye atlamak için gereken XP: `seviye × 100`.
- Seviye atlayınca grup içinde tebrik mesajı gönderilir.

---

## 🔧 Özelleştirme İpuçları

- **Metinleri değiştirmek** için `i18n.py` dosyasındaki `TEXTS` sözlüğünü
  düzenle — hem TR hem EN karşılığını güncellemeyi unutma.
- **Yeni komut eklemek** için `handlers/` altına yeni bir fonksiyon yaz,
  `main.py` içinde `app.add_handler(CommandHandler(...))` ile bağla.
- **Holder sayısı** için Solscan Pro API key almak istersen
  [pro-api.solscan.io](https://pro-api.solscan.io) üzerinden alıp
  `SOLSCAN_API_KEY` değişkenine ekle.

---

## ❓ Sorun Giderme

| Sorun | Çözüm |
|---|---|
| Bot mesajlara cevap vermiyor | `/setprivacy` → Disable yapıldı mı kontrol et |
| Captcha çalışmıyor | Bot grupta admin mi, "restrict members" yetkisi var mı kontrol et |
| Spam silinmiyor | Bot grupta "delete messages" yetkisine sahip mi kontrol et |
| `/price` "veri alınamadı" diyor | `CONTRACT_ADDRESS` doğru mu, DexScreener'da pair var mı kontrol et |
| Railway'de bot sürekli yeniden başlıyor | Variables sekmesinde `BOT_TOKEN` doğru girildi mi kontrol et, Deployments loglarına bak |

---

*Built to Climb 🐐 — $IBEX*
