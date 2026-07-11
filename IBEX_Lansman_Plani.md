# IBEX Coin — Lansman Öncesi Topluluk & Otomasyon Planı

**Marka:** Ibex Coin | **Sembol:** $IBEX | **Ağ:** Solana | **Tema:** Dağ keçisi (ibex) — zirveye tırmanış

---

## 1. Slogan Önerileri

| Dil | Slogan |
|---|---|
| TR | "Ibex, zirveye tırmanıyor." |
| TR | "Düşmez, sadece tırmanır." |
| EN | "Ibex Never Looks Down." |
| EN | "Built to Climb." |
| EN | "The Summit is Just the Start." |

Öneri: X biyografisinde ve logonun altında **"Built to Climb"** kullan — İngilizce global erişim için daha güçlü, Türkçe içerikte "Zirveye tırmanıyor" kullanılabilir.

---

## 2. Marka Kimliği Kontrol Listesi (Lansmandan önce bitmeli)
- [ ] Logo son hali (elindeki mevcut logo kullanılabilir, farklı boyutlarda export: 1024x1024, 512x512, favicon 64x64)
- [ ] Ticker/isim çakışma kontrolü (CoinMarketCap, CoinGecko, DEX'lerde "Ibex/IBEX" araması)
- [ ] Renk paleti: Sarı (#FFC72C) + Krem (#FFF8E7) + koyu kontrast metin
- [ ] Tokenomics taslağı: toplam arz, LP kilidi süresi, vergi (varsa), takım payı/vesting
- [ ] Linktree / basit landing page (isim, logo, slogan, sosyal linkler, kontrat adresi placeholder)

---

## SEÇENEK A — 7 GÜNLÜK HIZLI LANSMAN

| Gün | Görevler |
|---|---|
| **1** | X (Twitter) ve Telegram hesaplarını aç. Logo, banner, biyografi ("Built to Climb") ekle. Botu Telegram grubuna kur (karşılama/captcha/spam filtresi aktif). |
| **2** | Linktree/landing page yayınla. Tokenomics'i tek sayfalık görsel olarak paylaş (şeffaflık = güven). İlk teaser postu: "Something is climbing… 🐐" |
| **3** | Meme yarışması başlat (ödül: whitelist/airdrop yeri). Telegram'da sabit mesaj olarak kurallar + doğrulama talimatı. |
| **4** | 3-5 küçük/orta ölçekli Solana meme KOL'üyle iletişime geç (ücretli post veya shoutout). Countdown postu: "3 gün kaldı 🐐⛰️" |
| **5** | Topluluk AMA'sı (Telegram sesli sohbet veya X Space) — proje vizyonu, tokenomics, lansman saati duyurusu. |
| **6** | Son teaser'lar, whitelist/erken erişim listesi kapanışı, "24 saat kaldı" countdown, contract adresini ASLA önceden paylaşma (kopya kontrat riskine karşı). |
| **7** | **Lansman günü** — Kontrat deploy → LP ekle/kilitle → resmi kontrat adresini SADECE doğrulanmış kanallardan paylaş → Dexscreener linki → `/price` komutu aktif hale gelir → duyuru botu ile pinlenmiş mesaj. |

---

## SEÇENEK B — 4 HAFTALIK KAPSAMLI LANSMAN

### Hafta 1 — Temel Kurulum
- Marka kimliğini kesinleştir (logo, slogan, renkler)
- X, Telegram, (istersen Discord) hesaplarını aç
- Telegram botunu kur ve test et (karşılama, captcha, spam filtresi)
- Landing page / Linktree yayınla
- Tokenomics taslağını hazırla (henüz paylaşma, netleştir)

### Hafta 2 — İçerik & Erken Topluluk
- Günlük/gün aşırı X postu ritmine başla (meme + proje anlatısı karışık)
- Tokenomics'i resmi olarak paylaş (şeffaflık göster: LP kilidi, vesting)
- Whitelist/erken erişim formu aç (ilgi ölçmek ve ilk çekirdek topluluğu toplamak için)
- Küçük çaplı meme yarışması #1

### Hafta 3 — Büyüme & İşbirlikleri
- KOL/influencer görüşmeleri ve ilk shoutout'lar
- İkinci meme yarışması, daha büyük ödül
- Telegram'da aktif moderasyon + günlük "topluluk sıcaklığını" ölç (mesaj sayısı, yeni üye)
- Countdown içeriklerine başla: "2 hafta kaldı"

### Hafta 4 — Lansmana Hazırlık ve Lansman
- Gün 1-3: Son AMA/Space, son whitelist çağrısı
- Gün 4-5: "Yakında" yoğun teaser kampanyası, sahte kontrat adreslerine karşı uyarı postu yayınla
- Gün 6: Son kontroller (LP cüzdanı, kilit mekanizması, bot ayarları, `/price` için pair adresi hazır mı)
- Gün 7: **Lansman** — kontrat deploy, LP kilitleme, resmi duyuru, `/duyuru` komutuyla pinlenmiş mesaj, Dexscreener/price takibi başlat

---

## 3. Otomasyon Durumu (Telegram Botu)
Bot zaten hazır ve şu işlevleri otomatik yapıyor:
- Yeni üye karşılama + captcha doğrulama
- Spam/scam link filtreleme
- `/price` — Dexscreener'dan anlık veri (kontrat adresi eklendiğinde aktifleşir)
- `/duyuru` — admin duyurularını gruba yayınlar ve pinler

**Eksik/senin yapman gerekenler (otomatikleştirilemez, güvenlik gereği):**
- Kontrat deploy etmek ve LP kilitlemek (cüzdan/imza gerektirir, üçüncü bir tarafın yapamayacağı adım)
- KOL ile ücretli anlaşma görüşmeleri (insan teması gerekli)
- Resmi kontrat adresini paylaşma anı (taklit/scam kontrat riskine karşı bunu sen, doğrulanmış hesaptan yapmalısın)

---

## 4. Riskler — Baştan Not Edilmeli
- **Taklit kontrat riski:** Lansmandan önce "Ibex" adıyla sahte tokenlar oluşturulabilir. Resmi kontrat adresini sadece kendi doğrulanmış X/Telegram hesabından paylaş, hiçbir DM'e güvenme.
- **Botlar/whitelist manipülasyonu:** Whitelist formunda basit bir captcha/tekil e-posta veya Telegram ID kontrolü ekle.
- **Şeffaflık:** Tokenomics ve LP kilidi bilgisini erken paylaşmak güven inşa etmenin en hızlı yolu; gizli tutmak şüphe yaratır.
