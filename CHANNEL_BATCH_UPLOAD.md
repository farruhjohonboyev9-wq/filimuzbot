# 🎬 KANAL ORQALI BATCH FILM QO'SHISH

## 🚀 OSON USUL - Kanal link'i yubore, bot qo'shadi!

### 📝 Jarayon:

```
1️⃣  Bot'ga /kanaldan buyrug'i
2️⃣  Kanal link yuboring
3️⃣  Kanal'dan videolarni bot'ga forward qiling
4️⃣  /tayyor bosing
5️⃣  Har bitta video uchun ma'lumot kiriting
6️⃣  Bot avtomatik saqlaydi!
```

---

## 🎯 QO'L-QO'LAMDA REAL MISOL

### 1️⃣ Bot'ni ishga tushiring:

```bash
python channel_uploader.py
```

Yoki asosiy bot'da:

```bash
python filimuz.py
```

### 2️⃣ Bot'a yuboring:

```
/kanaldan
```

### 3️⃣ Kanal linkini yuboring:

**3 ta usul:**

**A) Telegram link:**
```
t.me/mening_filmlar
```

**B) @ username:**
```
@mening_filmlar
```

**C) Channel ID:**
```
-1001234567890
```

Bot javob beradi:
```
✅ KANAL QABUL QILINDI!

📺 Kanal: @mening_filmlar

Endi: Kanal'dan videolarni bot'ga forward qiling.
```

### 4️⃣ Kanaldan videolarni forward qiling:

Kanal'dan:
1. Video tanglang → Forward → Select Chat → Bot
2. Video bo'taqa'da forward qiling (1-2-3...)

Bot javob beradi har bitta video uchun:
```
✅ VIDEO #1 QABUL QILINDI

📹 File ID: BAACAgIAAxkDAAI...
📦 Hajm: 156.34 MB
📐 O'lcham: 1920x1080
⏰ Davomiylik: 148 min

Davom:
• Yana video forward qiling
• /tayyor - ma'lumot kiritish
• /bekor - bekor qilish
```

### 5️⃣ Tayyoq bo'lganda:

```
/tayyor
```

Bot taklif beradi:
```
✅ TAYYOR!

📊 Jami videolar: 5

Endi har bitta video uchun ma'lumot kiriting:

Format:
Title|Year|Rating|Genre|Director|Description|Key

📋 Misol:
Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish|inception

Video 1 uchun ma'lumot:
```

### 6️⃣ Ma'lumot kiritish (har bitta video):

**Video 1:**
```
Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish haqida film|inception
```

Bot:
```
✅ VIDEO #1 QO'SHILDI

🎬 Inception (2010)
⭐ 8.8/10

Video #2 uchun ma'lumot:
```

**Video 2:**
```
The Matrix|1999|8.7|Sci-Fi, Action|The Wachowskis|Neo haqiqat va simulyatsiya orasinda|matrix
```

Bot:
```
✅ VIDEO #2 QO'SHILDI

🎬 The Matrix (1999)
⭐ 8.7/10

Video #3 uchun ma'lumot:
```

Va shunaqa davom...

### 7️⃣ Barcha birka:

Terminal'da oxiri ko'rasiz:
```
✅ BARCHA FILMLAR QO'SHILDI!

✅ Qo'shilgan: 5 ta
💾 films_database.json ga saqlandi!
📊 Jami filmlar: 55

🔄 Bot'ni restart qiling:
Ctrl+C → python filimuz.py
```

---

## 📊 JO'NAT BO'YICHA:

### 5 ta video bo'lsa:

1. **/kanaldan** - 10 soniya
2. **Link yuboring** - 5 soniya  
3. **5 ta video forward** - 30 soniya
4. **/tayyor** - Instant
5. **5 ta metadata** - 2-3 daqiqa
6. **Bot saqlaydi** - 5 soniya

**Jami: 3-4 daqiqa!** ⚡

---

## 💡 TIPS

### 1. Sifat ketman bo'lsin!
```
Format to'g'ri:
Title|Year|Rating|Genre|Director|Description|Key
```

### 2. Key unique bo'lsin
```
✅ inception, inception_2, inception_4k
❌ inception (agar boshqa inception bor bo'lsa)
```

### 3. Description batafsil
```
✅ Cooper va jamoasi orzularga kirib g'oyalar o'g'irlashadi
❌ Batman filmi
```

### 4. Reyting IMDb'dan oling
https://www.imdb.com/

---

## 🔄 KANALDA MANFAA

### Nima uchun kanal?

✅ **Tashkiliy** - Videolarni bir joyga jamlash
✅ **Kolay** - Forward qilish sodda
✅ **Xavfsiz** - Kanal private bo'lishi mumkin
✅ **Batafsil** - Video meta'larni caption'da qo'yish mumkin

### Kanal sozlash:

```
1. Private channel yaratish
2. Bot'ni admin qilish (kerak emas, faqat qulaylik)
3. Videolarni uploadin qilish
4. Bot /kanaldan orqali oling
```

---

## ⚠️ XATOLAR

### ❌ "FORWARD QILINGAN VIDEO KERAK"
```
Sabab: Video'ni forward qilmangiz
Yechim: Kanal'dan video'ni forward qiling
```

### ❌ "VIDEO YO'Q"
```
Sabab: Hech qanday video forward qilmangiz
Yechim: Avval /kanaldan, keyin videolarni forward qiling
```

### ❌ "Noto'g'ri format"
```
Sabab: 7 ta qism kerak (| bilan)
Yechim: Title|Year|Rating|Genre|Director|Desc|Key
```

### ❌ "Noto'g'ri link"
```
Sabab: Link format noto'g'ri
Yechim: @username, t.me/username, yoki -1001234567890
```

### ❌ Batch'da xatolik?
```
Sabab: Metadata format noto'g'ri
Yechim: /bekor bosing va qayta boshlang
```

---

## 🎯 BOSHQA USULLAR

### A) Bitta-bitta film qo'shish:

```bash
python filimuz.py
/addfilm FILE_ID
Title|Year|Rating|...
```

### B) Avtomatik kanal monitor:

```bash
python channel_monitor.py
```

Kanal'ga videolar yuklanganda avtomatik xabar keladi.

### C) File ID utility:

```bash
python get_file_id.py
```

Har bitta videoni bo'y-bo'y olish uchun.

---

## 📚 QOLLANMALAR

- **Tezkor boshlash:** [START.md](START.md)
- **Bitta-bitta qo'shish:** [KANALDAN_FILM_QOSHISH.md](KANALDAN_FILM_QOSHISH.md)
- **50MB+ yechimi:** [KATTA_FILMLAR_QOLLANMA.md](KATTA_FILMLAR_QOLLANMA.md)

---

## ✅ TAYYOR!

Kanal linkini berib, batch'da filmlar qo'shishni boshlang! 🚀

```bash
python channel_uploader.py
```

Keyin bot'ga:
```
/kanaldan
```

**3-4 daqiqa - 10+ film qo'shiladi!** ⚡
