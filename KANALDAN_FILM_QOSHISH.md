# 🎬 TELEGRAM KANALDAN AVTOMATIK FILM QO'SHISH

## 📺 Qanday Ishlaydi?

Telegram kanalga video yuklasangiz, bot avtomatik ravishda `file_id` ni olib, filmga qo'shadi!

---

## 🚀 TEZKOR BOSHLASH

### 1️⃣ Telegram Kanal Ochish

```
1. Telegram'da yangi channel yarating:
   - Private yoki Public (tavsiya: Private)
   - Nom: Masalan "@mening_filmlar"

2. Bot'ni channel'ga admin qiling:
   - Channel Settings → Administrators
   - Add Administrator
   - @sizning_botingiz ni tanlang
   - Ruxsatlar: "Post Messages" dan boshqa hamma yo'q bo'lishi mumkin
```

### 2️⃣ Video Yuklash

```
1. Channel'ga video yuklang
2. Caption qo'shing (film nomi)
```

### 3️⃣ File ID Olish - 2 usul:

#### A) get_file_id.py orqali:
```bash
python get_file_id.py

# Bot'ga video'ni forward qiling yoki to'g'ridan jo'nating
# File ID terminal'da chiqadi
```

#### B) `/addfilm` command orqali (yangi!):
```
Bot'ga:
/addfilm BAACAgIAAxkDAAI...

# Keyin film ma'lumotlarini yuboring
```

---

## 💡 YANGI FEATURE: /addfilm buyrug'i

### Qanday ishlatish:

**1. File ID ni oling:**
```bash
python get_file_id.py
# Videoni bot'ga jo'nating
# File ID: BAACAgIAAxkDAAI... ni copy qiling
```

**2. `/addfilm` buyrug'i yuboring:**
```
/addfilm BAACAgIAAxkDAAI...
```

**3. Bot sizga** format ko'rsatadi:
```
✅ Film qo'shish boshlandi!

📝 Quyidagi formatda ma'lumotlarni yuboring:

Title|Year|Rating|Genre|Director|Description|Key

📋 Misol:
Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish haqida ajoyib film|inception

⚠️ Key - inglizcha, kichik harflar, probelsiz!
```

**4. Formatda yuboring:**
```
Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish haqida ajoyib film|inception
```

**5. Bot saqlaydi:**
```
✅ Film muvaffaqiyatli qo'shildi!

🎬 Inception (2010)
⭐ 8.8/10
🎭 Sci-Fi, Thriller
👤 Christopher Nolan
📝 Orzularga kirish haqida ajoyib...
🔑 Key: inception

💾 films_database.json ga saqlandi!

🔄 Bot'ni restart qiling
```

**6. Bot'ni restart qiling:**
```bash
# Terminal'da Ctrl+C bosing
python filimuz.py
```

---

## 📋 TO'LIQ MISOL

### Misol 1: Inception filmini qo'shish

**1. Video olish:**
- Inception filmini kanalga yuklang yoki mavjud bo'lsa

**2. File ID olish:**
```bash
python get_file_id.py
# Video'ni bot'ga forward qiling
# Output:
==============================================================
✅ VIDEO TOPILDI!
==============================================================
📹 File ID: BAACAgIAAxkDAAICXGWxxYZ1234567890abcdef
📦 Hajm: 156.34 MB
⏰ Davomiylik: 148 daqiqa
```

**3. Botga yuborish:**
```
/addfilm BAACAgIAAxkDAAICXGWxxYZ1234567890abcdef
```

**4. Ma'lumot yuborish:**
```
Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish haqida ajoyib film. Cooper va jamoasi orzularga kirib, g'oyalar o'g'irlashadi|inception
```

**5. Tasdiqlash:**
```
✅ Film muvaffaqiyatli qo'shildi!
```

**6. Restart:**
```bash
python filimuz.py
```

**7. Test:**
```
/list
1
# Video darhol yuboriladi!
```

---

### Misol 2: The Matrix filmini qo'shish

```
/addfilm BAACAgIAAxkDAAIBBGWyzzXXXaabbcc

The Matrix|1999|8.7|Sci-Fi, Action|The Wachowskis|Dasturchi Neo haqiqat va simulyatsiya o'rtasida tanlov qiladi|matrix
```

---

## 🎯 KANAL MONITOR (Avtomatik)

Agar kanaldan **avtomatik** film qo'shishni xohlasangiz:

### channel_monitor.py ishlatish:

```bash
python channel_monitor.py
```

Bu script:
1. ✅ Kanalga video yuklanganda avtomatik file_id ni oladi
2. ✅ Adminga xabar yuboradi
3. ✅ `/addfilm` buyrug'ini tayyorlaydi

**Output:**
```
============================================================
📺 TELEGRAM KANAL MONITOR
============================================================

✅ Bot ishga tushdi!
👥 Adminlar: [123456789]

📝 Qanday ishlaydi:
1. Kanalga video yuklang
2. Bot avtomatik file_id ni oladi
3. Adminga xabar yuboradi
4. Admin /addfilm bilan qo'shadi

🔄 Monitor ishlamoqda...
```

### Kanalga video yuklasangiz:

**Admin'ga keladi:**
```
📹 YANGI VIDEO KANALDA!

🎬 Nomi: Inception Trailer
📦 Hajm: 15.5 MB
⏰ Davomiylik: 2 daqiqa
📐 O'lcham: 1920x1080

📹 File ID:
BAACAgIAAxkDAAICXGWxxYZ...

💡 Botga qo'shish uchun:
/addfilm BAACAgIAAxkDAAICXGWxxYZ...
```

Keyin faqat `/addfilm` bosing va ma'lumotlarni yuboring!

---

## ⚙️ SOZLAMALAR

### Bot'ni ikkita process'da ishlatish:

**Terminal 1 - Asosiy bot:**
```bash
python filimuz.py
```

**Terminal 2 - Kanal monitor:**
```bash
python channel_monitor.py
```

Yoki faqat **asosiy bot**da `/addfilm` ishlating (kanal monitor kerak emas).

---

## 📊 FORMAT QOIDALARI

### Ma'lumot formati:
```
Title|Year|Rating|Genre|Director|Description|Key
```

### Har bir qism:

| Qism | Tavsif | Misol |
|------|--------|-------|
| **Title** | Film nomi | Inception |
| **Year** | Yili (raqam) | 2010 |
| **Rating** | Reyting (float) | 8.8 |
| **Genre** | Janr (vergul bilan) | Sci-Fi, Thriller |
| **Director** | Rezhissyor | Christopher Nolan |
| **Description** | Tavsif (ko'proq ma'lumot) | Orzularga kirish... |
| **Key** | Unique kalit (kichik harflar!) | inception |

### Key qoidalari:
- ✅ Kichik harflar: `inception`
- ✅ Raqamlar: `matrix2`
- ✅ Underscore: `dark_knight`
- ✅ Minus: `spider-man`
- ❌ Katta harflar: `Inception` ❌
- ❌ Probellar: `the matrix` ❌
- ❌ Belgilar: `film@2024` ❌

---

## 🔍 XATOLARNI TUZATISH

### ❌ "Film allaqachon mavjud"
```
Sabab: Key dublikat
Yechim: Boshqa key tanlang (inception_2, inception_hd, etc.)
```

### ❌ "Noto'g'ri format"
```
Sabab: | belgilari to'g'ri emas yoki 7 ta qism yo'q
Yechim: 
Inception|2010|8.8|Sci-Fi|Christopher Nolan|Tavsif|inception
1️⃣     |2️⃣  |3️⃣ |4️⃣   |5️⃣               |6️⃣    |7️⃣
```

### ❌ "Year va Rating raqam bo'lishi kerak"
```
Sabab: Year yoki Rating raqam emas
Yechim: Year = 2010 (raqam), Rating = 8.8 (float)
```

### ❌ "Key noto'g'ri"
```
Sabab: Key katta harflar yoki belgilar bor
Yechim: Faqat kichik harflar: inception, dark_knight
```

### ❌ "Sizda admin huquqi yo'q"
```
Sabab: Siz admin emassiz
Yechim: .env faylda ADMIN_IDS ga o'zingizni qo'shing
```

---

## 🎉 BEST PRACTICES

### 1. Film nomini to'g'ri yozing
```
✅ The Dark Knight
❌ dark knight
❌ DARK KNIGHT
```

### 2. Description batafsil bo'lsin
```
✅ Bruce Wayne Gotham shahrini Joker'dan himoya qiladi
❌ Batman filmi
```

### 3. Key unique bo'lsin
```
✅ dark_knight, dark_knight_2008, dk_2008
❌ batman (agar boshqa batman bor bo'lsa)
```

### 4. Genre aniq
```
✅ Sci-Fi, Action, Thriller
❌ Sci-fi
```

### 5. Rating IMDb dan oling
```
✅ 8.8 (IMDb: https://www.imdb.com/)
❌ 9.5 (o'ylab topish)
```

---

## 📚 QO'SHIMCHA MATERIALLAR

- **File ID olish:** [get_file_id.py](get_file_id.py)
- **Kanal monitor:** [channel_monitor.py](channel_monitor.py)
- **50MB+ yechimi:** [KATTA_FILMLAR_QOLLANMA.md](KATTA_FILMLAR_QOLLANMA.md)
- **Tezkor boshlash:** [TEZKOR_BOSHLASH.md](TEZKOR_BOSHLASH.md)

---

## ✅ XULOSA

### Umumiy jarayon:

1. ✅ **Channel yarating** va bot'ni admin qiling
2. ✅ **Video yuklang** kanalga
3. ✅ **File ID oling** - `python get_file_id.py`
4. ✅ **Bot'ga yuboring** - `/addfilm FILE_ID`
5. ✅ **Ma'lumot kiriting** - `Title|Year|Rating|...|Key`
6. ✅ **Restart qiling** - `python filimuz.py`
7. ✅ **Test qiling** - `/list` → raqam kiriting

**3-5 daqiqa - TAYYOR!** 🚀
