# 🚀 FILIMUZ BOT - SERVER DEPLOYMENT QOLLANMASI

## 📋 1. SERVER TAYYORLASH

### 1.1 SSH orqali serverga kirish
```bash
ssh root@YOUR_SERVER_IP
```

### 1.2 Tizimni yangilash
```bash
apt update && apt upgrade -y
```

### 1.3 Python va kerakli tools o'rnatish
```bash
apt install -y python3.12 python3.12-venv python3-pip git curl wget nano
```

### 1.4 Bot fayldirektoriyasini yaratish
```bash
cd /root
git clone https://github.com/YOUR_USERNAME/filimuz.git
cd filimuz
```

**YOKI qo'lda yuklash:**
1. Barcha fayllarini serverga `scp` orqali jaborgatish:
```bash
scp -r filimuz/ root@YOUR_SERVER_IP:/root/
```

---

## 🔐 2. KONFIGURATSIYA (.env)

### 2.1 .env faylni yaratish
```bash
nano /root/filimuz/.env
```

### 2.2 Quyidagi ma'lumotlarni kiriting:
```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_IDS=YOUR_ADMIN_ID_HERE
```

**CTRL+X ni bosing, Y ni bosing, ENTER ni bosing**

---

## 📦 3. VIRTUAL ENVIRONMENT VA PAKETLAR

### 3.1 Virtual environment yaratish
```bash
cd /root/filimuz
python3.12 -m venv venv
source venv/bin/activate
```

### 3.2 Requirements o'rnatish
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.3 Bot ishlashini tekshirish (test)
```bash
python filimuz.py
```

**Agar "Application started" ko'rinsa - hammasi yaxshi! ✅**
**Ctrl+C bosib to'xtating.**

---

## 🔄 4. SYSTEMD SERVICE O'RNATISH (24/7)

### 4.1 Service faylini o'rnatish
```bash
cp /root/filimuz/filimuz.service /etc/systemd/system/filimuz.service
```

### 4.2 Service ni reload qilish
```bash
systemctl daemon-reload
```

### 4.3 Service ni faollashtirish
```bash
systemctl enable filimuz
systemctl start filimuz
```

### 4.4 Statusni tekshirish
```bash
systemctl status filimuz
```

**Output:**
```
● filimuz.service
     Loaded: loaded
     Active: active (running)
```

---

## 📝 5. LOGLARNI KO'RISH

### 5.1 Real-time loglar
```bash
journalctl -u filimuz -f
```

### 5.2 Oxirgi 50 ta log
```bash
journalctl -u filimuz -n 50
```

### 5.3 Xatolarni topish
```bash
journalctl -u filimuz | grep ERROR
```

---

## 🔧 6. BOT BOSHQARUVI

### 6.1 Bot ishga tushirish
```bash
systemctl start filimuz
```

### 6.2 Bot to'xtatish
```bash
systemctl stop filimuz
```

### 6.3 Bot qayta ishga tushmasi
```bash
systemctl restart filimuz
```

### 6.4 Bot holatini tekshirish
```bash
systemctl status filimuz
```

---

## 🔄 7. BOT YANGILASH

### 7.1 Yangi cod yuklash
```bash
cd /root/filimuz
git pull origin main
```

**YOKI qo'l bilan:**
```bash
# Fayllarni saqlang
nano filimuz.py
# Kerakli o'zgartirishlarni qiling
# Ctrl+X, Y, ENTER
```

### 7.2 Paketlarni yangilash
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### 7.3 Bot qayta ishga tushmasi
```bash
systemctl restart filimuz
```

---

## ⚠️ 8. MUAMMOLARNI BARTARAF ETISH

### Muammo: Bot ishlamayapti
```bash
# 1. Status tekshiring
systemctl status filimuz

# 2. Loglarni ko'ring
journalctl -u filimuz -n 100

# 3. Bot qayta tushiramiz
systemctl restart filimuz
```

### Muammo: "Permission denied"
```bash
chmod +x /root/filimuz/startup.sh
```

### Muammo: "Module not found"
```bash
source /root/filimuz/venv/bin/activate
pip install -r requirements.txt
```

### Muammo: Port already in use
```bash
# Port 8000 ni tekshiring (agar web app bo'lsa)
lsof -i :8000
kill -9 PID_NUMBER
```

---

## 🔐 9. XAVFSIZLIK

### 9.1 Firewall sozlash (istegliga qarab)
```bash
# SSH port (22) ni oqish
ufw allow 22/tcp

# HTTP (80)
ufw allow 80/tcp

# HTTPS (443)
ufw allow 443/tcp

# Firewall ni yoqish
ufw enable
```

### 9.2 .env faylni himoya qilish
```bash
chmod 600 /root/filimuz/.env
```

### 9.3 Token ni maksimal himoyada saqlash
- ❌ Tokenni GitHub da joylamang
- ❌ Tokenni LogFiles da chiqarmang
- ✅ .env ni .gitignore da qo'shing

---

## 📊 10. MONITORING

### 10.1 Bot RAM/CPU dan o'qilishi
```bash
ps aux | grep filimuz
```

### 10.2 Disk joy tekshirish
```bash
df -h
```

### 10.3 Database o'lcham tekshirish
```bash
ls -lh /root/filimuz/database.json
```

---

## 🎯 11. BACKUP QILISH

### 11.1 Database backup
```bash
cp /root/filimuz/database.json /root/filimuz/database.backup.json
```

### 11.2 Avtomatik backup (cron)
```bash
crontab -e
```

Quyidagini qo'shing:
```
0 2 * * * cp /root/filimuz/database.json /root/filimuz/backups/database_$(date +\%Y\%m\%d).json
```

---

## ✅ JAMI CHECKLIST

- [ ] Python 3.12 o'rnatilgan
- [ ] .env faylida TOKEN va ADMIN_ID bor
- [ ] Virtual environment yaratilgan
- [ ] requirements.txt o'rnatilgan
- [ ] Bot test qilib ko'rilgan
- [ ] Systemd service o'rnatilgan
- [ ] Systemd xizmati faol va ishlayapti
- [ ] Loglar ko'rilgan, xato yo'q
- [ ] .env faylning ruxsatlari sozlangan (chmod 600)

---

## 📞 YORDAM

**Xatolarni tekshirish:**
```bash
journalctl -u filimuz -n 100
```

**Bot ishlayotganligini tekshirish:**
```bash
curl https://api.telegram.org/bot/getMe
```

---

**✨ BOT 24/7 ISHLAYAPTI!**
