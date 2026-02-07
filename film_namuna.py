"""
🎬 FILMLARNI QOSHISH UCHUN NAMUNA KOD

Bu faylni nusxa ko'chiring va o'zingizning filmingiz bilan almashtiring
"""

# NAMUNA 1: LOKAL VIDEO FAYL
# movies papkasida "myfilm.mp4" fayli bo'lishi kerak

"myfilm": {
    "title": "Mening Filmim",
    "year": 2024,
    "rating": 8.5,
    "janr": "Drama, Thriller",
    "director": "Director Name",
    "description": "Bu juda ajoyib film haqida qisqacha tavsif",
    "languages": ["python", "javascript"],
    "video": "./movies/myfilm.mp4"
},

# NAMUNA 2: YOUTUBE LINKI
# Video avtomatik yuklab olinadi (50MB gacha)

"film2": {
    "title": "Internet Film",
    "year": 2023,
    "rating": 7.8,
    "janr": "Action, Sci-Fi",
    "director": "John Doe",
    "description": "YouTube dan olinadigan film",
    "languages": ["python"],
    "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
},

# NAMUNA 3: SERIAL QISMLARI
# Serial uchun bir nechta qism

"serial1": {
    "title": "Serial - 1-qism",
    "year": 2024,
    "rating": 9.0,
    "janr": "Drama, Mystery",
    "director": "Serial Director",
    "description": "Serialning birinchi qismi",
    "languages": ["python", "cpp"],
    "video": "./movies/serial_ep1.mp4"
},

"serial2": {
    "title": "Serial - 2-qism",
    "year": 2024,
    "rating": 9.0,
    "janr": "Drama, Mystery",
    "director": "Serial Director",
    "description": "Serialning ikkinchi qismi",
    "languages": ["python", "cpp"],
    "video": "./movies/serial_ep2.mp4"
},

# NAMUNA 4: QISQA METRLI FILM

"shortfilm": {
    "title": "Qisqa Metrajli Film",
    "year": 2024,
    "rating": 7.5,
    "janr": "Comedy, Short",
    "director": "Young Director",
    "description": "15 daqiqalik qisqa film",
    "languages": ["javascript"],
    "video": "./movies/short.mp4"
}

"""
QANDAY ISHLATISH:

1. Yuqoridagi namunalardan birini tanlang
2. O'zingizning ma'lumotlaringiz bilan almashtiring
3. filimuz.py faylidagi movies = {...} ichiga qo'shing
4. Botni qayta ishga tushiring

ESDA TUTING:
- Video fayl hajmi: maksimum 50MB
- Video format: MP4 (h264)
- Film kaliti (masalan "myfilm") lotin harflarda, probelsiz
- Har bir film oxirida VERGUL (,) bo'lishi kerak
"""
