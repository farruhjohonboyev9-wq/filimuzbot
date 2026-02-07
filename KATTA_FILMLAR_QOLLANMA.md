# 🎬 50MB DAN KATTA FILMLAR: TO'LIQ QOLLANMA

## ⚡ TEZKOR YECHIM (Tavsiya etiladi)

### 1️⃣ Video'ni Telegram Channel'ga yuklang

**A) Private Channel yarating:**
```
1. Telegram'da yangi channel yarating (Private yoki Public)
2. Bot'ni channel'ga admin qiling (@BotFather'dan)
3. Video'ni channel'ga yuklang (2GB gacha!)
```

**B) File ID ni oling:**
```bash
# Terminal'da ishga tushiring:
python get_file_id.py

# Keyin:
# 1. Bot'ga video jo'nating (yoki channel'dan forward qiling)
# 2. File ID chiqadi - copy qiling
```

**C) JSON'ga qo'shing:**
```json
{
  "key": "avatar",
  "title": "Avatar",
  "year": 2009,
  "rating": 7.9,
  "janr": "Sci-Fi, Action",
  "director": "James Cameron",
  "description": "Pandora sayyorasida...",
  "languages": ["python"],
  "file_id": "BAACAgIAAxkDAAICXGWxxx..."  // ← SHU FILE_ID NI QOYING
}
```

**D) Bot'ni qayta ishga tushiring:**
```bash
# Ctrl+C bilan to'xtating
# Keyin yana ishga tushiring:
python filimuz.py
```

✅ **TAYYOR!** Film endi 50MB limitsiz yuboriladi!

---

## 🎯 ISHLATISH NAMUNALARI

### Misol 1: Telegram'dan File ID olish

```bash
# 1. get_file_id.py ni ishga tushiring
python get_file_id.py

# 2. Bot'ga video jo'nating
# Terminal'da ko'rasiz:

==============================================================
✅ VIDEO TOPILDI!
==============================================================
📹 File ID: BAACAgIAAxkDAAICXGWxxYZ1234567890abcdef
📦 Hajm: 156.34 MB
⏰ Davomiylik: 108 daqiqa
📐 O'lcham: 1920x1080

📋 JSON uchun kod:
--------------------------------------------------------------
  "file_id": "BAACAgIAAxkDAAICXGWxxYZ1234567890abcdef",
--------------------------------------------------------------

# 3. Copy/paste qiling JSON'ga!
```

### Misol 2: films_database.json'ga qo'shish

**Yangi film qo'shish:**
```json
{
  "films": [
    {
      "key": "inception",
      "title": "Inception",
      "year": 2010,
      "rating": 8.8,
      "janr": "Sci-Fi, Thriller",
      "director": "Christopher Nolan",
      "description": "Orzularga kirish...",
      "languages": ["python"],
      "file_id": "BAACAgIAAxkDAAICXGWxxx..."
    }
  ]
}
```

**Mavjud filmga file_id qo'shish:**
```json
{
  "key": "matrix",
  "title": "The Matrix",
  "video": "./movies/matrix.mp4",  // ← Bu eski
  "file_id": "BAACAgIAAxkDAAICXGWxxx..."  // ← Yangi qator qo'shing
}
```

---

## 🔄 FILE_ID NIMA VA QANDAY ISHLAYDI?

### Telegram File ID tizimi:

1. **Birinchi yuklarish:**
   - Video Telegram server'ga yuklanadi
   - Telegram unique ID beradi: `BAACAgIAAxkDAAI...`
   - Bu ID barcha Telegram'da amal qiladi

2. **Keyingi yuborishlar:**
   - Video qayta yuklanmaydi!
   - Faqat ID ishlatiladi (0.1 soniyada yuboriladi!)
   - 50MB limit yo'q (2GB gacha)

3. **Bot avtomatik saqlaydi:**
   - Film birinchi yuborilganda bot file_id ni eslaydi
   - films_database.json'ga yozadi
   - Keyingi safar avtomatik ishlatadi

---

## 📊 HAJM BO'YICHA STRATEGIYA

| Hajm | Yechim | Tezlik | Tavsiya |
|------|--------|--------|---------|
| 0-50 MB | Local fayl | ⚠️ Sekin | ✅ Oddiy |
| 50-500 MB | File ID | ⚡ Tez | ✅✅ Tavsiya |
| 500 MB - 2 GB | File ID | ⚡ Tez | ✅✅ Eng yaxshi |
| 2 GB+ | Google Drive | 🔗 Link | ⚠️ Tashqi |

---

## 💻 AMALIY QADAMLAR

### Qadam 1: Channel yarating
```
@FilimuzArchive nomli private channel
```

### Qadam 2: Bot'ni admin qiling
```
1. Channel Settings → Administrators
2. Add Administrator
3. @filimuz_bot ni tanlang
4. Ruxsatlar: Post Messages, Edit Messages
```

### Qadam 3: Video yuklang
```
1. Channel'ga video jo'nating
2. Video yuklanguncha kuting
```

### Qadam 4: File ID oling
```bash
# Terminal:
python get_file_id.py

# Bot'dan channel'dan video'ni forward qiling
# Yoki to'g'ridan-to'g'ri bot'ga jo'nating
```

### Qadam 5: JSON'ga qo'shing
```json
{
  "key": "yangi_film",
  "title": "Yangi Film",
  "file_id": "BAACAgIAAxk..."  // ← Copy qilgan ID
}
```

### Qadam 6: Bot'ni restart qiling
```bash
# Ctrl+C
python filimuz.py
```

### Qadam 7: Test qiling!
```
Bot'da: /list
Raqam kiriting: 1
Video darhol yuboriladi! ⚡
```

---

## 🎥 VIDEO SIQISH (Agar kerak bo'lsa)

### FFmpeg bilan (Windows):

**1. FFmpeg o'rnating:**
```powershell
# Chocolatey bilan:
choco install ffmpeg

# Yoki manual: ffmpeg.org/download.html
```

**2. Video'ni siqing:**
```bash
# 720p, 40MB atrofida
ffmpeg -i original.mp4 -vf scale=-2:720 -c:v libx264 -crf 26 -preset slow -b:v 600k -maxrate 600k -bufsize 1200k -c:a aac -b:a 96k compressed.mp4

# 480p, 25MB atrofida
ffmpeg -i original.mp4 -vf scale=-2:480 -c:v libx264 -crf 28 -preset slow -b:v 400k -maxrate 400k -bufsize 800k -c:a aac -b:a 64k compressed.mp4

# 360p, 15MB atrofida
ffmpeg -i original.mp4 -vf scale=-2:360 -c:v libx264 -crf 30 -preset slow -b:v 250k -maxrate 250k -bufsize 500k -c:a aac -b:a 64k compressed.mp4
```

### HandBrake bilan (GUI):

**1. Yuklab oling:** https://handbrake.fr/

**2. Sozlamalar:**
```
- Format: MP4
- Preset: Fast 480p30 (yoki 720p30)
- Video Codec: H.264
- Quality: RF 26-28
- Audio: AAC, 96kbps
```

**3. Start bosing!**

---

## 🔍 UMUMIY XATOLAR VA YECHIMLAR

### ❌ "File ID ishlamadi"
```
Sabab: File ID eskirgan yoki bot'da yo'q
Yechim: Yangi file_id oling (get_file_id.py)
```

### ❌ "Video juda katta (150MB)"
```
Sabab: Local fayl ishlatilmoqda, file_id yo'q
Yechim: File ID qo'shing films_database.json ga
```

### ❌ "Video topilmadi"
```
Sabab: Channel'dan o'chirilgan
Yechim: Qayta yuklang va yangi file_id oling
```

### ❌ "Bot admin emas"
```
Sabab: Channel'da bot admin emas
Yechim: Channel Settings → Add Administrator
```

---

## 📖 QO'SHIMCHA MANBA'LAR

- **Telegram Bot API:** https://core.telegram.org/bots/api
- **FFmpeg Documentation:** https://ffmpeg.org/documentation.html
- **HandBrake Guide:** https://handbrake.fr/docs/

---

## 💡 PRO MASLAHATLAR

1. **File ID ni doim saqlang** - Telegram file_id hech qachon o'zgarmaydi
2. **Channel private qiling** - Faqat siz ko'rishingiz mumkin
3. **Bot avtomatik saqlaydi** - Film birinchi yuborilganda file_id saqlanadi
4. **2GB limitdan foydalaning** - Telegram 2GB gacha videolarni qo'llab-quvvatlaydi
5. **Sifatni saqlang** - Video sifatini kamaytirmang, Telegram avtomatik optimize qiladi

---

## ✅ XULOSA

**ENG OSON YECHIM:**
1. `python get_file_id.py` - ishga tushiring
2. Bot'ga video jo'nating
3. File ID ni copy qiling
4. films_database.json'ga qo'shing
5. Bot'ni restart qiling

**NATIJA:**
- ⚡ 0.1 soniyada video yuboriladi
- 📦 50MB+ filmlar muammosiz
- 💾 2GB gacha qo'llab-quvvatlash
- 🔄 Avtomatik saqlash

**OMAD! 🚀**
