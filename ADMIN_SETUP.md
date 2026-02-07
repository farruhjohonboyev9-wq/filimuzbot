# 👤 ADMIN PANEL - Sozlash Yo'riqnomasi

## 1️⃣ Admin ID ni olish

Telegram da o'zingizning user ID ni bilish uchun:

### Usul 1: @userinfobot (Eng oson)
1. Telegram da **@userinfobot** ni qidiring
2. `/start` yuboring
3. Bot sizga ID ni ko'rsatadi (masalan: `123456789`)

### Usul 2: @getmyid_bot
1. **@getmyid_bot** ni qidiring
2. `/start` yuboring
3. Sizning ID ni ko'rsatadi

---

## 2️⃣ Admin ID ni qo'shish

### config.py faylida:

1. `config.py` faylini oching
2. `ADMIN_IDS` listiga o'zingizning ID ni qo'shing:

```python
ADMIN_IDS = [
    123456789,  # 👈 O'zingizning ID
    987654321,  # 👈 Boshqa admin (agar kerak bo'lsa)
]
```

### Yoki .env faylida:

1. `.env` faylini oching
2. Quyidagi qatorni qo'shing:

```
ADMIN_IDS=123456789,987654321
```

Ko'p admin bo'lsa, vergul bilan ajratib yozing.

---

## 3️⃣ Admin Panel Komandalar

Botni qayta ishga tushirganingizdan keyin:

### 🔐 Admin Panel
```
/admin - Admin panel ochish
```

### 📊 Statistika
```
/stats - Bot statistikasi
```
Ko'rsatiladi:
- Jami foydalanuvchilar
- Oxirgi 24 soatda faol
- Jami buyruqlar
- Yuborilgan videolar
- Bot  ishga tushgan vaqt

### 👥 Foydalanuvchilar
```
/users - Foydalanuvchilar ro'yxati
```
Ko'rsatiladi:
- Top 20 ta faol foydalanuvchi
- Har birining username
- Buyruqlar soni
- Videolar soni

### 📢 Broadcast
```
/broadcast Sizning xabaringiz
```
Masalan:
```
/broadcast Yangi Wednesday seriya qo'shildi! 🎬
```

⚠️ **Eslatma:** Barcha foydalanuvchilarga yuboriladi!

### 📝 Loglar
```
/logs - Bot loglari (oxirgi 50 qator)
```

---

## 4️⃣ Xavfsizlik

🔐 Admin parolini hech kimga bermang!
🔐 `.env` faylini GitHub ga yuklang!
🔐 `config.py` da admin ID larni yashiring

---

## 5️⃣ Test qilish

1. Botni ishga tushiring:
```powershell
python filimuz.py
```

2. Telegram da botga `/admin` yuboring

3. Agar admin bo'lsangiz - admin panel ochiladi ✅
4. Agar yo'q bo'lsa - "Admin huquqi yo'q" ❌

---

## 6️⃣ Database

Bot avtomatik ravishda `database.json` faylini yaratadi:

```json
{
    "users": {
        "123456789": {
            "user_id": 123456789,
            "username": "username",
            "first_name": "Ism",
            "joined_at": "2026-02-06T...",
            "last_active": "2026-02-06T...",
            "commands_used": 5,
            "videos_watched": 3
        }
    },
    "stats": {
        "total_users": 1,
        "total_commands": 10,
        "total_videos_sent": 5,
        "bot_started": "2026-02-06T..."
    }
}
```

⚠️ Bu faylni o'chirmaslik!

---

## 7️⃣ Muammolar

### "Admin huquqi yo'q" xatosi:
- ID to'g'ri kiritilganini tekshiring
- Botni qayta ishga tushiring
- `.env` yoki `config.py` ni tekshiring

### Broadcast ishlamayapti:
- Admin ekanligingizni tekshiring
- Xabar formati: `/broadcast Matn`

### Database topilmadi:
- Bot avtomatik yaratadi
- Birinchi marta `/start` yuborganingizda yaratiladi

---

## 🎯 Tayyor!

Endi sizda to'liq admin panel bor! 🚀

**Admin qobiliyatlari:**
- ✅ Statistika ko'rish
- ✅ Foydalanuvchilarni ko'rish
- ✅ Barcha foydalanuvchilarga xabar yuborish
- ✅ Bot loglarini ko'rish
- ✅ To'liq nazorat

---

## 📞 Qo'shimcha yordam

Agar muammo bo'lsa:
1. Botni qayta ishga tushiring
2. Admin ID ni tekshiring
3. .env va config.py fayllarni tekshiring

**Omad!** 🎬
