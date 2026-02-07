# 🎬 Film Tavsiya Telegram Boti

Kodli kinolar haqida ma'lumot beruvchi, ko'p funksiyali Telegram botining to'liq implementatsiyasi.

## ✨ Xususiyatlari

### 🎥 Asosiy Funksiyalar
- 📋 Barcha filmlarni ko'rish
- ⭐ Eng yaxshi filmlar
- 🎲 Tasodifiy film tavsiyasi
- 💻 Dasturlash tiliga qarab filmlar (Python, C++, C#, PHP, Java)
- 🔍 Film nomi orqali qidirish
- 📥 YouTube/Instagram video yuklovchi

### 👤 Foydalanuvchi Xususiyatlari
- ⭐ **Sevimlilar tizimi** - Yoqtirgan filmlarni saqlash
- 📜 **Tarix** - Ko'rilgan filmlar tarixi
- 👤 **Profil** - Shaxsiy statistika va ma'lumotlar
- 💰 **Ball tizimi** - Faollik uchun ballar
- 🌐 **Ko'p tillik** - O'zbek, Rus, Ingliz

### 📊 Social Funksiyalar
- ⭐ **Baholash** - Filmlarni 1-10 baholash
- 💬 **Izohlar** - Filmlar haqida fikr bildirish
- 🏆 **Reyting** - Jamoa baholari va statistika
- 👑 **Leaderboard** - Top foydalanuvchilar
- 🔥 **Trendlar** - Eng ko'p ko'rilgan filmlar

### 💎 Premium Xususiyatlar
- 📺 HD video yuklovchi
- 🎬 Cheksiz sevimlilar
- 🚫 Reklama yo'q
- ⭐ Yangi filmlar birinchi bo'lib
- 🤖 Shaxsiy tavsiyalar

### 🛠️ Admin Panel
- 📊 Detаl statistika
- 👥 Foydalanuvchilar boshqaruvi
- 📢 Broadcast xabarlar
- 💎 Premium boshqaruvi
- 📝 Log monitoring

## 🚀 Boshlash

### 1. Talablarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. .env faylini sozlash
```bash
# .env fayliga Telegram Bot Tokenni qo'shing
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
```

### 3. Botni ishga tushirish
```bash
python filimuz.py
```

## 📝 Komandalar

### Asosiy Komandalar
| Komanda | Tavsifi |
|---------|---------|
| `/start` | Botni boshlash |
| `/list` | Barcha filmlar ro'yxati |
| `/top` | Eng yaxshi filmlar |
| `/random` | Tasodifiy film tavsiyasi |
| `/kodli` | Faqat kodli kinolar |
| `/help` | Yordam |

### Foydalanuvchi Komandalar
| Komanda | Tavsifi |
|---------|---------|
| `/profile` | Shaxsiy profil |
| `/favorites` | Sevimlilar ro'yxati |
| `/history` | Ko'rilgan filmlar |
| `/settings` | Sozlamalar |

### Statistika Komandalar
| Komanda | Tavsifi |
|---------|---------|
| `/toprated` | Eng yuqori baholangan filmlar |
| `/mostwatched` | Eng ko'p ko'rilgan filmlar |
| `/leaderboard` | Top foydalanuvchilar |

### Dasturlash Tillari
| Komanda | Tavsifi |
|---------|---------|
| `/python` | Python filmlar |
| `/cpp` | C++ filmlar |
| `/csharp` | C# filmlar |
| `/php` | PHP filmlar |
| `/java` | Java filmlar |

### Video Yuklovchi
| Komanda | Tavsifi |
|---------|---------|
| `/ig [link]` | YouTube/Instagram video yuklash |

### Admin Komandalar
| Komanda | Tavsifi |
|---------|---------|
| `/admin` | Admin panel |
| `/stats` | Bot statistikasi |
| `/users` | Foydalanuvchilar ro'yxati |
| `/broadcast [text]` | Hammaga xabar yuborish |
| `/givepremium [user_id]` | Premium berish |
| `/revokepremium [user_id]` | Premium olish |
| `/logs` | Bot loglari |

## 🎮 Foydalanish

### Film Tanlash
1. `/list` buyrug'i bilan filmlarni ko'ring
2. Film raqamini yuboring (masalan: `1`)
3. Inline tugmalar orqali:
   - ▶️ Videoni ko'rish
   - ⭐ Sevimlilar ro'yxatiga qo'shish
   - ⭐ Baholash (1-10)
   - 💬 Izoh qoldirish

### Ball Tizimi
- 🎬 Video ko'rish: **+3 ball**
- ⭐ Sevimlilar qo'shish: **+5 ball**
- ⭐ Baholash: **+10 ball**
- 💬 Izoh qoldirish: **+15 ball**

## 📦 Fayl Tuzilmasi

```
filimuz/
├── filimuz.py                   # Asosiy bot fayli
├── database.py                  # Database boshqaruvi
├── config.py                    # Konfiguratsiya
├── translations.py              # Ko'p tillik
├── database.json                # Ma'lumotlar bazasi
├── films_database.json          # Filmlar bazasi (JSON)
├── requirements.txt             # Python kutubxonalar
├── .env                         # Environment o'zgaruvchilar
├── FILMLAR_QOSHISH.md          # Filmlar qo'shish qo'llanmasi
├── KATTA_FILMLAR_YECHIM.md     # 50MB+ filmlar yechimi
├── KATTA_FILMLAR_QOLLANMA.md   # To'liq qo'llanma
├── get_file_id.py              # File ID olish utility
├── banner/                      # Bot bannerlari
├── downloads/                   # Vaqtinchalik yuklamalar
└── movies/                      # Film fayllari

```

## 🎬 Filmlar Qo'shish

### Oddiy Film (< 50MB):
```json
{
  "key": "inception",
  "title": "Inception",
  "year": 2010,
  "rating": 8.8,
  "janr": "Sci-Fi",
  "director": "Christopher Nolan",
  "description": "Orzularga kirish...",
  "languages": ["python"],
  "video": "./movies/inception.mp4"
}
```

### Katta Film (50MB+) - FILE_ID USULI:
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
  "file_id": "BAACAgIAAxkDAAICXGWxxx..."  // ← Telegram file_id
}
```

### File ID qanday olish:
```bash
# 1. Utility'ni ishga tushiring
python get_file_id.py

# 2. Bot'ga video jo'nating (yoki channel'dan forward)
# 3. File ID ni copy qiling
# 4. films_database.json ga qo'shing
```

📖 **To'liq qo'llanma:** [KATTA_FILMLAR_QOLLANMA.md](KATTA_FILMLAR_QOLLANMA.md)

## ⚡ 50MB+ Filmlar Uchun Yechim

### Muammo:
- Telegram bot API: **50MB limit** ❌
- Filmlar ko'pincha 100MB+ 😔

### Yechim - Telegram File ID:
- ✅ **2GB gacha** qo'llab-quvvatlash
- ✅ **Cheksiz tezlik** (0.1 soniyada)
- ✅ **Avtomatik saqlash**
- ✅ **Qayta yuklamaslik**

### Qanday ishlaydi:
1. Video birinchi yuborilganda Telegram server'ga yuklanadi
2. Telegram unique `file_id` beradi
3. Bot file_id ni saqlaydi (JSON ga)
4. Keyingi safar faqat file_id ishlatadi → instant yuboriladi! ⚡

### Amaliy Qadamlar:
```bash
# 1. File ID olish utility
python get_file_id.py

# Bot'ga video jo'nating → File ID chiqadi

# 2. JSON'ga qo'shing:
"file_id": "BAACAgIAAxkDAAICXGWxxx..."

# 3. Bot avtomatik ishlatadi!
```

📚 **Batafsil:** [KATTA_FILMLAR_YECHIM.md](KATTA_FILMLAR_YECHIM.md)

## 🔧 Texnologiyalar

- **Python 3.8+**
- **python-telegram-bot** - Telegram Bot API
- **yt-dlp** - Video yuklovchi
- **asyncio** - Asinxron dasturlash
- **JSON** - Ma'lumotlar bazasi

## 📊 Database Tuzilmasi

```json
{
  "users": {},           // Foydalanuvchilar
  "favorites": {},       // Sevimlilar
  "ratings": {},         // Baholash
  "comments": {},        // Izohlar
  "watch_history": {},   // Tarix
  "premium_users": [],   // Premium a'zolar
  "user_languages": {},  // Til sozlamalari
  "stats": {}           // Statistika
}
```

## 🌐 Ko'p Tillik

Bot 3 ta tilda ishlaydi:
- 🇺🇿 O'zbek
- 🇷🇺 Русский
- 🇬🇧 English

Tilni `/settings` orqali o'zgartirish mumkin.

## 💡 Yangi Xususiyatlar (v2.0)

- ✅ Inline keyboard interface
- ✅ Sevimlilar va tarix tizimi
- ✅ Baholash va izohlar
- ✅ Ko'p tillik qo'llab-quvvatlash
- ✅ Premium tizim
- ✅ Ball va reyting tizimi
- ✅ Kengaytirilgan admin panel
- ✅ Real-time statistika
- ✅ Social funksiyalar

## 🤝 Hissa Qo'shish

Pull request'lar xush kelibsiz! Katta o'zgarishlar uchun avval issue oching.

## 📄 Litsenziya

MIT License

## 📞 Aloqa

Savollar yoki takliflar bo'lsa, issue oching yoki admin bilan bog'laning.

---

**Made with ❤️ for the coding community**
- AlphaGo
- Hardcode
- Pirates of Silicon Valley

## 🛠️ Texnologiyalar

- Python 3.8+
- python-telegram-bot (20.5+)
- Async/Await

## 📌 Eslatmalar

- Token `.env` faylida saqlang
- Tortutga hech kimga token bermang
- Bot 24/7 ishga tushirilishi mumkin
