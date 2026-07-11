# IBEX Coin Telegram Botu

## Özellikler
- 👋 Yeni üye karşılama + matematik captcha ile bot/spam hesap doğrulama
- 🛡️ Link ve scam anahtar kelime filtreleme (admin hariç herkes için)
- 💰 `/price` — Dexscreener üzerinden anlık fiyat, likidite, FDV bilgisi
- 📢 `/duyuru <mesaj>` — sadece adminler kullanabilir, mesajı gruba yayınlar ve pinler

---

## 1. Bot Token Alma
1. Telegram'da **@BotFather**'a git
2. `/newbot` yaz, ismini ve kullanıcı adını belirle (örn: `MirCoinBot`)
3. Sana verilen token'ı kopyala (örn: `123456:AAExxxx`)

## 2. Botu Grubuna Ekleme
1. Botu Telegram grubuna üye olarak ekle
2. Grup ayarlarından botu **admin** yap (özellikle şu izinler gerekli):
   - Kullanıcıları kısıtlama/atma (ban/restrict)
   - Mesaj silme
   - Mesaj pinleme

## 3. Kendi Telegram ID'ni Öğrenme
Telegram'da **@userinfobot**'a mesaj at, sana ID'ni verecek. Bu ID'yi
`ADMIN_IDS` değişkenine ekleyeceksin.

## 4. Railway'de Yayınlama (ÜCRETSİZ, ÖNERİLEN)

1. https://railway.app adresine git, GitHub hesabınla giriş yap
2. Bu klasördeki dosyaları bir GitHub reposuna yükle (veya Railway'in
   "Deploy from local folder" / CLI seçeneğini kullan)
3. Railway'de **New Project → Deploy from GitHub repo** seç
4. **Variables** sekmesine gidip `.env.example` dosyasındaki değişkenleri
   gerçek değerlerle birlikte ekle:
   - `BOT_TOKEN`
   - `ADMIN_IDS`
   - `TOKEN_NAME`
   - `DEXSCREENER_PAIR_ADDRESS` (lansmandan sonra dolduracaksın)
   - `VERIFY_TIMEOUT_SECONDS`
5. Railway otomatik olarak `requirements.txt`'i kurup `Procfile`'daki
   komutla botu başlatacak
6. Deploy bittiğinde botun grubunda aktif olacak (7/24 çalışır, bilgisayarını
   açık tutmana gerek yok)

**Railway CLI ile alternatif (daha hızlı):**
```bash
npm i -g @railway/cli
railway login
cd mir_bot
railway init
railway up
railway variables set BOT_TOKEN=xxx ADMIN_IDS=xxx TOKEN_NAME=MIR
```

## 5. Yerelde Test Etme (opsiyonel)
```bash
pip install -r requirements.txt
export BOT_TOKEN=xxx
export ADMIN_IDS=xxx
python main.py
```

---

## Sonradan Yapılacaklar
- Token lansmanından sonra `DEXSCREENER_PAIR_ADDRESS` değişkenini
  gerçek pair adresiyle güncelle (Railway → Variables → düzenle → otomatik restart)
- `SCAM_KEYWORDS` listesini (main.py içinde) topluluğunda gördüğün yeni
  scam kalıplarına göre genişletebilirsin
- `/duyuru` komutunu grup içinde admin hesabınla test et

## Notlar
- Bot sadece **kısıtlama/atma** yapar, hiçbir zaman ban (kalıcı) uygulamaz —
  doğrulamayan kullanıcı sadece gruptan çıkarılır, tekrar katılabilir
- Fiyat verisi Dexscreener'ın herkese açık API'sinden gelir, ek API key gerekmez
