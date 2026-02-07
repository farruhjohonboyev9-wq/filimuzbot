# 📺 KATTA HAJMLI FILMLAR UCHUN YECHIM

50MB dan katta filmlar uchun 3 ta yechim:

---

## 1️⃣ TELEGRAM CHANNEL ORQALI (Tavsiya etiladi) 🎯

### Qadam 1: Telegram Channel yarating
1. Telegram'da yangi private/public channel yarating
2. Bot'ni channel'ga admin qiling

### Qadam 2: Film videosini channel'ga yuklang
1. Channel'ga video yuborib qo'ying (2GB gacha)
2. Video'ga o'ng tugma bosing → Copy Message Link
3. File ID ni olish uchun forward_channel_id qo'shing

### Qadam 3: films_database.json da file_id qo'shing

```json
{
  "key": "interstellar",
  "title": "Interstellar",
  "year": 2014,
  "rating": 8.6,
  "janr": "Sci-Fi, Drama",
  "director": "Christopher Nolan",
  "description": "Kosmik sayohat",
  "languages": ["python"],
  "video": "channel_file_id",  // Yoki file_id
  "file_id": "BAACAgIAAxkDAAICXGWxxx...",  // Video file_id
  "channel_id": "@your_channel"  // Channel username
}
```

### File ID ni qanday olish:

```python
# forward_test.py
from telegram import Bot

bot = Bot(token="YOUR_BOT_TOKEN")

# Channel'dan video forward qiling
# Keyin file_id ni console'da ko'rasiz
async def get_file_id():
    # Video file_id ni ko'rish
    updates = await bot.get_updates()
    print(updates)

# Yoki oddiy qilib:
# 1. Bot'ga video jo'nating
# 2. Log'da file_id ko'rinadi
```

---

## 2️⃣ VIDEO HOSTINGDAN LINK QILISH

### Google Drive:
```json
{
  "video": "https://drive.google.com/file/d/FILE_ID/view",
  "video_type": "gdrive"
}
```

### OneDrive, Dropbox, Mega:
```json
{
  "video": "https://www.dropbox.com/s/xxx/video.mp4?dl=1",
  "video_type": "direct_link"
}
```

### YouTube (Private):
```json
{
  "video": "https://www.youtube.com/watch?v=XXXXX",
  "video_type": "youtube"
}
```

---

## 3️⃣ VIDEO SIQISH (FFmpeg)

### Telegram uchun optimal (720p, 40MB):
```bash
ffmpeg -i input.mp4 \
  -vf scale=-2:720 \
  -c:v libx264 \
  -crf 26 \
  -preset slow \
  -b:v 600k \
  -maxrate 600k \
  -bufsize 1200k \
  -c:a aac \
  -b:a 96k \
  output.mp4
```

### 480p, 30MB:
```bash
ffmpeg -i input.mp4 \
  -vf scale=-2:480 \
  -c:v libx264 \
  -crf 28 \
  -preset slow \
  -b:v 400k \
  -maxrate 400k \
  -bufsize 800k \
  -c:a aac \
  -b:a 64k \
  output.mp4
```

### 360p, 15-20MB (eng kichik):
```bash
ffmpeg -i input.mp4 \
  -vf scale=-2:360 \
  -c:v libx264 \
  -crf 30 \
  -preset slow \
  -b:v 250k \
  -maxrate 250k \
  -bufsize 500k \
  -c:a aac \
  -b:a 64k \
  output.mp4
```

---

## 4️⃣ BO'LAKLARGA BO'LIB YUBORISH

Katta filmni qismlarga bo'lib yuborish:

```bash
# Har 10 daqiqadan kesish
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 00:10:00 -f segment output_part%03d.mp4
```

films_database.json da:
```json
{
  "key": "inception",
  "title": "Inception",
  "parts": [
    "./movies/inception_part1.mp4",
    "./movies/inception_part2.mp4",
    "./movies/inception_part3.mp4"
  ]
}
```

---

## 5️⃣ TELEGRAM FILE_ID USULI (Eng tez) ⚡

### Qanday ishlaydi:
1. Video birinchi marta yuklanganda Telegram file_id beradi
2. Keyingi yuborishlarda faqat file_id ishlatiladi (soniyada yuboriladi!)

### Database'ga qo'shish:
```python
# Bot birinchi yuborishda file_id ni saqlaydi
if video_message:
    file_id = video_message.video.file_id
    # database.json ga saqlash
    save_file_id(film_key, file_id)
```

---

## ⚙️ BOTGA FILE_ID QOSHISH

filimuz.py ga qo'shing:

```python
async def send_video_by_key(query, context, user_id, film_key):
    film = movies[film_key]
    
    # 1. FILE_ID mavjudmi?
    if 'file_id' in film and film['file_id']:
        try:
            await query.message.reply_video(
                video=film['file_id'],
                caption=f"🎬 {film['title']}"
            )
            return
        except:
            pass
    
    # 2. LOCAL FAYL
    if 'video' in film:
        # ... mavjud kod
```

---

## 📊 HAJM BO'YICHA TAVSIYALAR

| Sifat | Hajm | Telegram | Tavsiya |
|-------|------|----------|---------|
| 4K/1080p | 200MB+ | ❌ | Google Drive link |
| 720p | 80-150MB | ❌ | Channel file_id |
| 480p | 30-60MB | ⚠️ | Siqish kerak |
| 360p | 15-30MB | ✅ | To'g'ridan-to'g'ri |
| 240p | 5-15MB | ✅ | Eng yaxshi |

---

## 🎬 AMALIY MISOL

### A) HandBrake (GUI) bilan:
1. HandBrake yuklab oling: https://handbrake.fr/
2. Video faylni oching
3. Preset: "Fast 480p30"
4. Video Codec: H.264
5. Quality: RF 26-28
6. Audio: AAC, 96kbps
7. Start!

### B) Online Converter:
- CloudConvert.com
- Online-Convert.com
- FreeConvert.com

**Settings:**
- Format: MP4
- Codec: H.264
- Resolution: 480p yoki 360p
- Bitrate: 500-800 kbps
- Audio: AAC 96kbps

---

## 💡 ENG YAXSHI YECHIM (tavsiya)

### KICHIK FILMLAR (< 50MB):
```json
"video": "./movies/film.mp4"
```

### KATTA FILMLAR (> 50MB):
```json
"file_id": "BAACAgIAAxkDAAI...",
"channel_id": "@mening_kino_channel"
```

### JUDA KATTA (> 2GB):
```json
"video": "https://drive.google.com/file/d/xxxx/view",
"video_type": "gdrive"
```

---

## 🚀 TEZKOR START

1. **Telegram Channel ochish:**
   ```
   - @mening_filmlar nomli channel yarating
   - Bot'ni admin qiling
   - Video'larni yuklang
   ```

2. **File ID olish:**
   ```python
   # Bot'ga video yuboring
   # Log'da file_id ni ko'ring
   ```

3. **JSON'ga qo'shing:**
   ```json
   "file_id": "BAACAgIAAxk..."
   ```

4. **Bot avtomatik ishlaydi!** ✅

---

## 📞 Qo'shimcha Yordam

Agar muammo bo'lsa:
1. Avval video'ni siqing (HandBrake)
2. Telegram channel orqali yuklang
3. File ID ni saqlang
4. Profit! 🎉

**Omad tilaymiz! 🚀**
