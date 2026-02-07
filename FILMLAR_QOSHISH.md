# 🎬 Botga Yangi Filmlar Qo'shish Yo'riqnomasi

## 📋 Ikki xil usul:

### 1️⃣ **LOKAL VIDEO FAYLLAR** (Tavsiya etiladi)
### 2️⃣ **YOUTUBE/INTERNET LINKLAR**

---

## 1️⃣ LOKAL VIDEO FAYLLAR QOSHISH

### Qadam 1: Video faylni tayyorlash

Video faylni **movies** papkasiga joylashtiring:

```
filimuz/
├── movies/
│   ├── wednesday1.mp4  ✅ (mavjud)
│   ├── wednesday2.mp4  ✅ (mavjud)
│   ├── YANGI_FILM.mp4  ⬅️ Sizning yangi filmingiz
```

**⚠️ Muhim:**
- Video fayl hajmi: **maksimum 50MB** (Telegram cheklovi)
- Format: **MP4** (h264 codec)
- Agar katta bo'lsa, siqing:
  ```bash
  ffmpeg -i input.mp4 -vcodec h264 -acodec aac -b:v 800k output.mp4
  ```

### Qadam 2: filimuz.py fayliga film qo'shish

`filimuz.py` faylini oching va `movies = {` qismiga yangi film qo'shing:

```python
movies = {
    # ... mavjud filmlar ...
    
    # YANGI FILMINGIZ - bu yerga qo'shing:
    "inception": {
        "title": "Inception",
        "year": 2010,
        "rating": 8.8,
        "janr": "Sci-Fi, Thriller, Kodli",
        "director": "Christopher Nolan",
        "description": "Orzu o'g'irlash haqida ajoyib film",
        "languages": ["python", "javascript"],  # ixtiyoriy
        "video": "./movies/inception.mp4"  # Video fayl yo'li
    },
    
    # Yana bir film misoli:
    "matrix": {
        "title": "The Matrix",
        "year": 1999,
        "rating": 8.7,
        "janr": "Sci-Fi, Action, Kodli",
        "director": "Wachowski Brothers",
        "description": "Virtual reallik haqida ajoyib film",
        "languages": ["python", "cpp"],
        "video": "./movies/matrix.mp4"
    }
}
```

### Qadam 3: Botni qayta ishga tushirish

```bash
# Agar bot ishlayotgan bo'lsa, to'xtating (Ctrl+C)
# Keyin qayta ishga tushiring:
python filimuz.py
```

---

## 2️⃣ YOUTUBE/INTERNET LINKLARDAN QOSHISH

Video faylni yuklamasdan to'g'ridan-to'g'ri YouTube linkini qo'yishingiz mumkin:

```python
movies = {
    "interstellar": {
        "title": "Interstellar",
        "year": 2014,
        "rating": 8.6,
        "janr": "Sci-Fi, Drama",
        "director": "Christopher Nolan",
        "description": "Kosmik sayohat haqida film",
        "languages": ["python"],
        "video": "https://www.youtube.com/watch?v=zSWdZVtXT7E"  # YouTube link
    }
}
```

**⚠️ Eslatma:** 
- YouTube videodan avtomatik yuklab oladi
- 50MB dan katta bo'lsa, xatolik beradi
- Internet bo'lishi shart

---

## 📝 FILM STRUKTURASI TUSHUNTIRISH

```python
"film_kaliti": {  # Ichki nom (lotin harflarda, probelsiz)
    "title": "Film Nomi",           # Ko'rinadigan nom
    "year": 2024,                    # Chiqish yili
    "rating": 8.5,                   # Reyting (0-10)
    "janr": "Horror, Comedy",        # Janrlar (vergul bilan)
    "director": "Director Ismi",     # Rejissyor
    "description": "Qisqacha...",    # Tavsif
    "languages": ["python", "js"],   # Dasturlash tillari (ixtiyoriy)
    "video": "./movies/fayl.mp4"     # Video yo'li YOKI YouTube link
}
```

### Majburiy maydonlar:
- ✅ `title` - Film nomi
- ✅ `year` - Yil
- ✅ `rating` - Reyting
- ✅ `janr` - Janr
- ✅ `director` - Rejissyor
- ✅ `description` - Tavsif
- ✅ `video` - Video fayl yoki link

### Ixtiyoriy:
- `languages` - Dasturlash tillari (filtr uchun)

---

## 🎯 TO'LIQ MISOL

### 1. Video faylni joylashtiring:
```
movies/spiderman.mp4  (45MB)
```

### 2. filimuz.py ga qo'shing:

Quyidagi kod qismini toping:
```python
movies = {
    "wednesday8": {
        ...
    }  # ⬅️ Bu yerdan keyin qo'shing
}
```

Va yangi filmni qo'shing:
```python
movies = {
    "wednesday8": {
        ...
    },  # ⬅️ VERGULNI UNUTMANG!
    
    # YANGI FILM:
    "spiderman1": {
        "title": "Spider-Man: No Way Home",
        "year": 2021,
        "rating": 8.7,
        "janr": "Action, Adventure, Marvel",
        "director": "Jon Watts",
        "description": "Spider-Man multiverse haqida ajoyib film",
        "languages": ["python", "javascript"],
        "video": "./movies/spiderman.mp4"
    }
}
```

### 3. Botni qayta ishga tushiring

```bash
python filimuz.py
```

### 4. Botda tekshiring

Telegram botda:
1. `/list` - Yangi film ro'yxatda ko'rinadi
2. Raqamni yuboring (masalan: `9`)
3. Video yuboriladi

---

## ⚠️ KENG TARQALGAN XATOLAR

### ❌ Xato 1: Video fayl topilmadi
```
❌ Video fayl topilmadi: ./movies/film.mp4
```
**Yechim:** Fayl nomini to'g'ri yozing va movies papkasida borligini tekshiring

### ❌ Xato 2: Video juda katta
```
❌ Video juda katta (85.5MB)
```
**Yechim:** Video faylni siqing:
```bash
ffmpeg -i input.mp4 -vcodec h264 -b:v 800k output.mp4
```

### ❌ Xato 3: SyntaxError
```
SyntaxError: invalid syntax
```
**Yechim:** 
- Vergullarni tekshiring
- Qo'shtirnoqlarni tekshiring
- Qavslarni to'g'ri yopganingizni tekshiring

---

## 📚 KO'P FILMLAR QOSHISH

Bir nechta filmni birdan qo'shish:

```python
movies = {
    # Mavjud filmlar...
    
    # YANGI FILMLAR TO'PLAMI:
    "film1": {...},
    "film2": {...},
    "film3": {...},
    "film4": {...},
}
```

---

## 🎬 VIDEO TAYYORLASH BUYRUGLAR

### FFmpeg bilan siqish (800KB/s):
```bash
ffmpeg -i input.mp4 -vcodec h264 -acodec aac -b:v 800k -maxrate 800k output.mp4
```

### Sifatni saqlagan holda siqish:
```bash
ffmpeg -i input.mp4 -vcodec h264 -crf 28 -preset slow output.mp4
```

### Video kesgish (daqiqa 5-10):
```bash
ffmpeg -i input.mp4 -ss 00:05:00 -to 00:10:00 -c copy output.mp4
```

### Videoni kichiklantirish (480p):
```bash
ffmpeg -i input.mp4 -vf scale=-2:480 -c:v libx264 -crf 23 output.mp4
```

---

## 📞 Yordam

Agar muammo bo'lsa:
1. `database.json` ni o'chiring va qayta boshlang
2. Bot loglarini tekshiring
3. Video fayl hajmini tekshiring (50MB dan kam bo'lishi kerak)

**Omad tilaymiz! 🚀**
