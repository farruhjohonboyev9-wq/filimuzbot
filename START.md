# ⚡ KANALDANFILIM QO'SHISH - 2 DAQIQA!

## 🎬 HA! Bot avtomatik qo'shadi!

Kanal ga video tashlasangiz, bot file_id ni oladi va siz faqat ma'lumot kiritasiz!

---

## 🚀 BOSHLASH

### 1️⃣ Kanal yaratdingiz ✅

### 2️⃣ Endi video tashlang:

Kanalga video yuklang (istalgan hajmda, 2GB gacha)

### 3️⃣ File ID oling - ENG OSON USUL:

```bash
# Terminal 1:
python get_file_id.py
```

Bot ishga tushadi. Endi:
- Kanaldan videoni bot'ga **forward** qiling
- Yoki to'g'ridan-to'g'ri bot'ga video yuboring

Terminal'da ko'rasiz:
```
✅ VIDEO TOPILDI!
📹 File ID: BAACAgIAAxkDAAI...
```

**File ID ni copy qiling!**

### 4️⃣ Botga ma'lumot yuboring:

```bash
# Terminal 2 (yoki bitta terminal'da):
# Bot'ni avval ishga tushiring:
python filimuz.py
```

Bot'ga (privat chat):
```
/addfilm BAACAgIAAxkDAAI...
```

Bot javob beradi:
```
✅ Film qo'shish boshlandi!

Ma'lumotlarni yuboring:
Title|Year|Rating|Genre|Director|Description|Key
```

Ma'lumot yuboring:
```
Avatar|2009|7.9|Sci-Fi, Action|James Cameron|Pandora sayyorasida ajoyib sarguzasht|avatar
```

Bot:
```
✅ Film muvaffaqiyatli qo'shildi!
💾 films_database.json ga saqlandi!
🔄 Bot'ni restart qiling
```

### 5️⃣ Bot'ni restart qiling:

```bash
# Terminal'da Ctrl+C
python filimuz.py
```

### 6️⃣ Test qiling!

```
/list
# Ko'rasiz: yangi film ro'yxatda!

Raqam kiriting: 1
# Video DARHOL yuboriladi! ⚡
```

---

## 💡 KEYINGI SAFAR

Keyingi filmda:
1. Kanalga video yuklang ✓
2. `python get_file_id.py` ishga tushiring (agar to'xtatgan bo'lsangiz)
3. Video'ni bot'ga forward qiling → File ID oling
4. `/addfilm FILE_ID` → Ma'lumot kiriting
5. Bot restart → Tayyor!

**Juda oson!** 🎉

---

## 📋 FORMATNI ESLAB QOLING:

```
Title|Year|Rating|Genre|Director|Description|Key

Misol:
Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish|inception
```

**7 ta qism, | bilan ajratilgan!**

---

## 🎯 IKKITA OSON USUL

### Usul 1: Har safar get_file_id.py (tavsiya)
```bash
# Har safar video yuklasangiz:
python get_file_id.py
# Video forward qiling
# File ID ni oling
# /addfilm bilan qo'shing
```

### Usul 2: channel_monitor.py (avtomatik)
```bash
# Bir marta ishga tushiring:
python channel_monitor.py

# Bundan keyin kanalga video yuklasangiz,
# sizga avtomatik xabar keladi file_id bilan!
```

---

## ✅ TAYYOR!

Endi siz:
- ✅ Kanalga video yuklaysiz
- ✅ Bot file_id ni oladi
- ✅ Siz `/addfilm` bilan qo'shasiz
- ✅ **50MB+ filmlar muammosiz!** (file_id orqali 2GB gacha)
- ✅ **Tez yuboriladi!** (instant, Telegram cloud'dan)

**Barcha tayyor! Filmlar qo'shishni boshlang! 🚀**

---

## 📞 Yordam Kerakmi?

📖 To'liq qo'llanma: [KANALDAN_FILM_QOSHISH.md](KANALDAN_FILM_QOSHISH.md)
