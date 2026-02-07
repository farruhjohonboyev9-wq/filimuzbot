# 👨‍💼 PROFESSIONAL ADMIN PANEL - QOLLANMA

**Telegram Filimuz Botiga Professional Administratsiya Dashboard**

---

## 📋 MUNDARIJA

1. [Admin Panel Kirish](#admin-panel-kirish)
2. [Asosiy Dashboard](#asosiy-dashboard)
3. [Statistika Moduli](#statistika-moduli)
4. [Foydalanuvchilar Boshqaruvi](#foydalanuvchilar-boshqaruvi)
5. [Film Boshqaruvi](#film-boshqaruvi)
6. [Premium Sistema](#premium-sistema)
7. [Broadcast Sistema](#broadcast-sistema)
8. [Sistema Monitoringi](#sistema-monitoringi)
9. [Analytics](#analytics)
10. [Database Management](#database-management)

---

## 🔐 ADMIN PANEL KIRISH

### Kirish Usuli

```bash
/admin
```

**Shartlar:**
- Admin ID config.py ga ro'yxatga olingan bo'lishi kerak
- Faqat zarurlashtirilgan administrator foydalanishi mumkin

### Admin ID ni o'rnatish

**config.py:**
```python
ADMIN_IDS = [123456789, 987654321]  # O'zingizning ID ni qo'shing
```

**ID ni topish:**
1. @userinfobot ga /start yuboring
2. O'z ID ingizni oling
3. config.py ga qo'shing

---

## 🏠 ASOSIY DASHBOARD

Admin panelga kirgandan keyin siz 8 ta asosiy modulga ruhsat olinadi:

### 📊 Dashboard Tugmalari

```
┌─────────────────────────────┐
│ 👨‍💼 ADMIN PANEL              │
├─────────────────────────────┤
│ [📊 STATISTIKA] [👥 USERS]   │
│ [🎬 FILMLAR]    [💎 PREMIUM] │
│ [📢 BROADCAST]  [🔧 SISTEMA] │
│ [📈 ANALYTICS]  [🗂️ DATABASE] │
└─────────────────────────────┘
```

---

## 📊 STATISTIKA MODULI

### Umumiy Statistika

**Tasvir:**
- Jami foydalanuvchilar
- Premium foydalanuvchilar
- Jami filmlar
- Video ko'rilgan soni
- Database hajmi
- API Status
- Bot Status

**Misol Output:**
```
📊 STATISTIKA

👥 Foydalanuvchilar: 150
💎 Premium: 25
🎬 Jami filmlar: 50
📹 Video ko'rilgan: 5000

💾 Database: 2.5 MB
⏰ Vaqt: 07.02.2024 10:45:23

SYSTEM INFO:
🔋 API Status: ✅ Active
🌐 Bot Status: ✅ Online
📦 Python version: 3.12+
```

### Chuqur Statistika

**Neler uchun:**
- Kunlik/Haftalik/Oylik trend
- Top filmlar
- Engagement metrics
- Premium daromadi

---

## 👥 FOYDALANUVCHILAR BOSHQARUVI

### 1. User Qidirish

**Qo'llaniladigan operatsiyalar:**
- User ID orqali qidirish
- @username orqali qidirish
- User statistikasi ko'rish

**Qidirish Natijalari:**
```
🔍 USER QIDIRISH

ID: 123456789
Username: @username
Birinchi xabar: 2024-01-15
Oxirgi xabar: 2024-02-07
Premium: ✅ 5 kun qoldi
Videos: 45 ko'rilgan
Status: 🟢 Aktiv

[Block] [Premium] [Delete]
```

### 2. Top Users

**Filtrlash Turlari:**
1. **Video ko'rilgan (TOP 10)**
   - 🥇 @user1 - 523 videos
   - 🥈 @user2 - 412 videos
   - 🥉 @user3 - 398 videos

2. **Rating bermagan (TOP 5)**
   - ⭐ @user6 - 125 rating
   - ⭐ @user7 - 98 rating

3. **Yan Foydalanuvchilar**
   - Bugun: 5 ta
   - Hafta: 23 ta
   - Oy: 87 ta

### 3. User Operatsiyalari

**Quyidagi amallarni bajarishingiz mumkin:**

| Operatsiya | Tabrif | Asosyan |
|-----------|--------|---------|
| **Block** | Userni blokировка | Spam/abuse |
| **Premium** | Premium berish/olish | Premium tariff |
| **Delete** | Profilni o'chirish | Ikki marta so'roq |
| **Message** | Aniq xabar yuborish | Odishlash |
| **Stats** | User statistikasi | Analitika |

---

## 🎬 FILM BOSHQARUVI

### 1. Film Qo'shish

**Format:**
```
Nomi|Yil|Reyting|Janr|Direktor|Tavsif|Kalit
```

**Misol:**
```
Inception|2010|8.8|Sci-Fi|Christopher Nolan|Xayollar o'lami|inception
```

**Talab olunadigan maydonlar:**
- ✅ Nomi (20-100 belgi)
- ✅ Yil (4 raqam)
- ✅ Reyting (1-10)
- ✅ Janr
- ✅ Direktor
- ✅ Tavsif (10-500 belgi)
- ✅ Kalit (unique)

### 2. Filmlar Ro'yxati

**Tasvir:**
- Barcha filmlar
- Paging (20 ta har sahifada)
- Search funksiyasi
- Edit/Delete tugmalari

**Misol:**
```
📋 FILMLAR RO'YXATI (1-20)

1. Inception (2010) ⭐ 8.8
2. Matrix (1999) ⭐ 8.7
3. Avatar (2009) ⭐ 7.8
...

Jami: 50 ta
```

### 3. Film Amallar

**Quyidagi amallar:**
- ➕ Film qo'shish
- ✏️ Film tahrir
- 🗑️ Film o'chirish
- 🔍 Duplikat tekshirish
- 📤 Export JSON
- 📥 Import JSON

### 4. Film Importi/Exporti

**Export:**
```bash
# Barcha filmlar JSON ga
admin_films_export
```

**Import:**
```bash
# JSON dan filmlar
admin_films_import
```

---

## 💎 PREMIUM SISTEMA

### 1. Premium Status

**Joriy Statistika:**
```
💎 PREMIUM BOSHQARUVI

STATISTIKA:
• Aktiv premium: 25
• Yangi: +3 (bugun)
• Daromad: 250,000 so'm
• O'rtacha vaqt: 90 kun
```

### 2. Premium Berish

**Tariflar:**
```
• 1 oy - 10,000 so'm ⏱️ 30 kun
• 3 oy - 25,000 so'm ⏱️ 90 kun
• 6 ay - 45,000 so'm ⏱️ 180 kun
• 1 yil - 80,000 so'm ⏱️ 365 kun
• LIFETIME - 500,000 so'm ✨ Abadiy
• BEPUL - 7 kun test ⭐
```

**Qanday berish:**
1. User ID yuboring
2. Tariff tanlang
3. Tasdiqlang
4. Beriladi ✅

### 3. Premium Olish

**Shartlar:**
- Maniy bo'lgan premium o'chiriladi
- Foydalanuvchi bilgilanadi
- Tarix qayd olunadi

---

## 📢 BROADCAST SISTEMA

### 1. Xabar Yuborish

**Kim uchun:**
```
• 1️⃣ Barcha foydalanuvchilar
• 2️⃣ Premium foydalanuvchilar
• 3️⃣ Aktiv foydalanuvchilar
• 4️⃣ Aniq grup
```

### 2. Xabar Tipi

**Tiplar:**
- 📝 Text
- 🎬 Video
- 🖼️ Rasm
- 🎵 Audio
- 📄 Fayl
- 🎛️ Mix

### 3. Formatting

**HTML Tags:**
```html
<b>Bold</b>
<i>Italic</i>
<u>Underline</u>
<code>Code</code>
<pre>Preformatted</pre>
<a href="https://example.com">Link</a>
```

**Misol:**
```html
📢 <b>Oхли muxbar:</b>

<i>Yangi filmlar qo'shildi!</i>

<b>Hozirgi:</b>
• Avatar 2 - <a href="film://avatar2">ko'shing</a>
• Matrix Resurrection - <a href="film://matrix">ko'shing</a>

<code>Premium diskaunti: 30%</code>
```

### 4. Broadcast Tarix

**Tahlil:**
- Yuborilgan: X ta
- O'qilgan: X%
- Feedback: X ta
- Xatolar: X ta

---

## 🔧 SISTEMA MONITORINGI

### 1. Asosiy Status

```
🔧 SISTEMA BOSHQARUVI

STATUS:
• API: ✅ Online
• Database: ✅ OK
• Storage: ✅ 500 MB bosh
• Uptime: 99.9%
```

### 2. Loglar

**Log ko'rish:**
```
📋 SYSTEM LOGS (OXIRGI 10)

[2024-02-07 10:45:23] ✅ Bot started
[2024-02-07 10:45:45] 👤 User #12345 /start
[2024-02-07 10:46:12] 🎬 Film view: inception
[2024-02-07 10:47:33] ⭐ Rating added: 5
[2024-02-07 10:48:55] 💬 Comment added
[2024-02-07 10:49:12] 💎 Premium activated
[2024-02-07 10:50:23] 🔍 Search: 'Matrix'
[2024-02-07 10:51:45] 📥 Film added: Avatar
[2024-02-07 10:52:18] ✅ Database synced
[2024-02-07 10:53:09] 🟢 All systems online

ERROR COUNT: 0 ta
WARNING COUNT: 2 ta
```

### 3. Sistema Operatsiyalari

| Operatsiya | Tasvir | Ruhsat |
|-----------|--------|--------|
| **Cache Clear** | Keshni tozalash | ♻️ |
| **Backup** | Ma'lumotlar zaxirasi | 💾 |
| **Optimize** | Bazani optimizasiya | ⚙️ |
| **Restart** | Botni qayta ishga tushirish | 🔄 |
| **Logs Download** | Loglarni yuklab olish | 📥 |

---

## 📈 ANALYTICS

### 1. Foydalanuvchi Analytics

```
📈 ANALYTICS

FOYDALANUVCHI ANALYTICS:
📊 Bugungi yangi: +5
📊 Haftalik o'rtacha: 8
📊 Oylik trend: ⬆️ +20%
```

### 2. Content Analytics

```
CONTENT ANALYTICS:
🎬 Eng ko'p ko'rilgan: The Dark Knight
⭐ Eng yaxshi rated: Inception (8.8)
💬 Eng ko'p izohlar: Avatar
```

### 3. Grafylar va Chartlar

**Dostupnye:** 
- Kunlik view stats
- Haftalik user growth
- Oylik revenue
- Genre distribution

---

## 🗂️ DATABASE MANAGEMENT

### 1. Database Fayllar

```
🗂️ DATABASE MANAGEMENT

FAYLLAR:
📄 database.json: 2.5 MB
📄 films_database.json: 1.2 MB
📄 telegrambot.json: 0.8 MB

Jami: 4.5 MB
```

### 2. Backup Sistema

**Backup Yaratish:**
```
💾 BACKUP YARATILDI

⏰ 07.02.2024 10:45:23

BACKUP QILINGAN:
✅ database.json
✅ films_database.json
✅ telegrambot.json

📦 Jami: 3 ta fayl
📍 Joylashuvi: backups/
```

### 3. Database Tozalash

**Tozalanadigan narsalar:**

```
🧹 DATABASE TOZALASH

1. Nofaol foydalanuvchilar (30 kundan ko'p): 45 ta
   ├─ O'chiriladi: 30 ta
   └─ Saqlanadi: 15 ta (premium)

2. Duplikat yozuvlar: 5 ta
   └─ O'chiriladi

3. Bo'sh yozuvlar: 2 ta
   └─ O'chiriladi

4. Temp fayllar: 12 ta
   └─ O'chiriladi

Tozalash hajmi: ~250 KB
```

### 4. Database Repair

```
🔧 DATABASE TA'MIR

TEKSHIRILYAPTI:
✅ Sintaksis - OK
✅ Schema - OK
✅ Indeks - OK
✅ Integralligi - OK
✅ Kodlash - OK

TOPILGAN MUAMMOLAR: 0️⃣ Yo'q

STATISTIKA:
📊 Jami yozuvlar: 5000+
📊 Fayl o'lchami: 2.5 MB
⏱️ Tekshirish vaqti: 2.3 sec
```

---

## ⚙️ SOZLASH VA INTEGRATSIYA

### Admin Panelni Aktivlash

**filimuz.py ga qo'shish:**

```python
from admin_integration import setup_admin_handlers

async def main():
    app = Application.builder().token(TOKEN).build()
    
    # Admin handlerlari o'rnatish
    setup_admin_handlers(app)
    
    # Boshqa handlerlari...
    
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
```

### Config Sozlash

**config.py:**
```python
# Admin IDs
ADMIN_IDS = [
    123456789,  # Admin 1
    987654321,  # Admin 2
]

# Admin tizimlari
ADMIN_FEATURES = {
    'user_management': True,
    'film_management': True,
    'premium_system': True,
    'broadcast': True,
    'database_tools': True,
    'analytics': True,
}

# Logging
ADMIN_LOGS = 'admin_logs.json'
BACKUP_DIR = 'backups/'
```

---

## 🔐 XAVFSIZLIK

### Admin Protokoli

1. **Avtentifikatsiya**
   - Faqat Admin IDs bo'yicha
   - Token orqali himoyalangan
   - IP filtering (ixtiyoriy)

2. **Audit Log**
   - Barcha operatsiyalar qayd olunadi
   - Kim qanday qilgan - tahlil
   - Qaytarish mumkinligi

3. **Qayta Tasdiq**
   - Muhim operatsiyalar: Delete, Block, Premium
   - "TASDIQLA" tugmasini bosish

### Xavfsizlik Bo'yicha Tavsiyalar

✅ **Qiling:**
- Admin panelni faqat trusted userlarga bering
- Logglarni muntazam tekshiring
- Backup qiling har hafta
- Strong token ishlating

❌ **Qilmang:**
- Admin password yuborma'ng
- Birdan ko'p administrator bermang
- SQL injection risk
- Public DB ma'lumotlari

---

## 📞 QOLLAB-QUVVATLASH

### Bot Status Tekshirish

```bash
/admin → Sistema → Status
```

### Muammolar

| Muammo | Yechimi |
|--------|---------|
| Admin panel ochilmayapti | Admin IDs tekshiring config.py da |
| Database xatosi | Repair tugmasini bosing |
| API offline | Bot restartini bosing |
| Slow response | Database tozalang |

---

## 📝 LOG VA EXPORT

### Export Formatlar

**JSON:**
```json
{
  "exported_at": "2024-02-07T10:45:23",
  "total_users": 150,
  "premium_users": 25,
  "total_films": 50,
  "total_videos_watched": 5000,
  "average_rating": 7.5
}
```

**CSV:**
- User statistikasi
- Film ma'lumotlari
- Premium tarihchasi

---

## 🎯 BEST PRACTICE

1. **Haftalik Maintenance**
   - Database optimize qiling
   - Loglar tozalang
   - Backup yaratilsin

2. **Oylik Review**
   - Statistikani tahlil qiling
   - Premium daromadni ko'ring
   - User feedback qayta kurting

3. **Xavfsizlik Audit**
   - Admin amallarini tekshiring
   - Nofaol userlarni o'chirib chiqing
   - Premium davomi tekshiring

---

**👨‍💼 Professional Administratsiya Panel**  
**Filimuz Bot v2.0**  
**2024 - ∞**
