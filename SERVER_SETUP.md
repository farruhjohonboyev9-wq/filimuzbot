# 🚀 Botni Serverga Joylashtirish

## 📋 Tayyorgarlik

### 1. Kerakli fayllar:
- ✅ `filimuz.py` - Bot kodi
- ✅ `requirements.txt` - Python paketlar
- ✅ `.env` - Bot tokeni
- ✅ `Procfile` - Server uchun
- ✅ `runtime.txt` - Python versiyasi
- ✅ `movies/` - Video fayllar papkasi

---

## 🌐 VARIANT 1: Railway (TAVSIYA - BEPUL, OSON)

### Afzalliklari:
- ✅ **500 soat** bepul har oy
- ✅ Oson sozlash
- ✅ GitHub bilan integratsiya
- ✅ Avtomatik deploy

### Qadamlar:

#### 1. GitHub ga yuklash:
```powershell
# Git o'rnatilganini tekshiring
git --version

# Agar yo'q bo'lsa: https://git-scm.com/download/win

# Git sozlash
git init
git add .
git commit -m "Initial commit"

# GitHub da yangi repository yarating: https://github.com/new
# Keyin:
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

#### 2. Railway ga deploy:
1. **Railway.app** ga kiring: https://railway.app/
2. GitHub bilan login qiling
3. **New Project** → **Deploy from GitHub repo**
4. Repository ni tanlang
5. **Environment Variables** ga o'ting:
   - `TELEGRAM_BOT_TOKEN` = `sizning_bot_tokeningiz`
6. **Deploy** tugmasini bosing

✅ **Tayyor!** Bot 24/7 ishlaydi!

---

## 🐧 VARIANT 2: Linux VPS Server (Ubuntu)

### Keraklilar:
- VPS server (DigitalOcean, Vultr, AWS, etc.)
- Ubuntu 20.04+

### Qadamlar:

#### 1. Serverga ulanish:
```bash
ssh root@your_server_ip
```

#### 2. Python va kerakli paketlarni o'rnatish:
```bash
# Sistema yangilash
sudo apt update && sudo apt upgrade -y

# Python va pip
sudo apt install python3 python3-pip python3-venv -y

# Git
sudo apt install git -y
```

#### 3. Botni serverga yuklash:
```bash
# Uy papkasiga o'tish
cd ~

# GitHub dan klonlash (yoki fayl ko'chirish)
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME

# Yoki FileZilla/SCP orqali fayllarni ko'chiring
```

#### 4. Virtual environment yaratish:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. .env faylini yaratish:
```bash
nano .env
```
Ichiga qo'ying:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```
Saqlash: `Ctrl+X`, `Y`, `Enter`

#### 6. Botni test qilish:
```bash
python3 filimuz.py
```
Ctrl+C bilan to'xtating (agar ishlasa)

#### 7. Systemd service yaratish (24/7 ishlatish):
```bash
sudo nano /etc/systemd/system/filmbot.service
```

Ichiga kiriting:
```ini
[Unit]
Description=Film Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/REPO_NAME
Environment="PATH=/root/REPO_NAME/venv/bin"
ExecStart=/root/REPO_NAME/venv/bin/python3 /root/REPO_NAME/filimuz.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Saqlash: `Ctrl+X`, `Y`, `Enter`

#### 8. Service ni ishga tushirish:
```bash
# Service ni reload
sudo systemctl daemon-reload

# Service ni yoqish
sudo systemctl enable filmbot

# Service ni ishga tushirish
sudo systemctl start filmbot

# Status tekshirish
sudo systemctl status filmbot

# Loglarni ko'rish
sudo journalctl -u filmbot -f
```

#### 9. Kerakli komandalar:
```bash
# Botni to'xtatish
sudo systemctl stop filmbot

# Botni qayta ishga tushirish
sudo systemctl restart filmbot

# Loglarni ko'rish
sudo journalctl -u filmbot -f

# Service ni o'chirish
sudo systemctl disable filmbot
```

---

## ☁️ VARIANT 3: Render (Bepul, Oson)

1. **Render.com** ga kiring: https://render.com/
2. **New** → **Web Service**
3. GitHub bilan bog'lang
4. Repository ni tanlang
5. Settings:
   - **Name**: filmbot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python filimuz.py`
6. **Environment Variables**:
   - `TELEGRAM_BOT_TOKEN` = `sizning_tokeningiz`
7. **Create Web Service**

⚠️ **Eslatma:** Render bepul rejada har 15 daqiqada uxlab qoladi, lekin botlar uchun muammo emas.

---

## 🔧 VARIANT 4: PythonAnywhere

1. **PythonAnywhere** ga kiring: https://www.pythonanywhere.com/
2. **Beginner** (bepul) rejani tanlang
3. **Dashboard** → **Files** → fayllarni yuklang
4. **Bash console** ochib:
```bash
pip install --user -r requirements.txt
```
5. **Always-on tasks** ga o'ting (⚠️ pullik):
   - Command: `python3 /home/username/filimuz.py`

⚠️ **Muammo:** Bepul rejada 24/7 ishlamaydi.

---

## 📦 Video Fayllar Masalasi

### ⚠️ Muhim:
Video fayllar (movies/) serverga joylashtirish murakkab, chunki:
- Fayllar hajmi katta (50MB x 21 film = ~1GB)
- GitHub 100MB dan katta fayllarni qabul qilmaydi

### ✅ Yechim 1: Git LFS (Large File Storage)
```bash
# Git LFS o'rnatish
git lfs install

# Video fayllarni LFS ga qo'shish
git lfs track "*.mp4"
git add .gitattributes
git add movies/*.mp4
git commit -m "Add video files"
git push
```

### ✅ Yechim 2: Cloud Storage (Tavsiya)
Video fayllarni cloud ga yuklang:
- **Google Drive** + public link
- **Dropbox**
- **AWS S3**
- **Cloudinary**

Keyin kodda URL ga o'zgartiring:
```python
"video": "https://drive.google.com/uc?id=FILE_ID"
```

### ✅ Yechim 3: SCP/SFTP orqali serverga ko'chirish
```bash
# Windowsdan Linux serverga
scp -r movies/ root@your_server_ip:/root/filimuz/
```

---

## 🔐 Xavfsizlik

### .env faylini himoyalash:
```bash
# .gitignore ga qo'shilganini tekshiring
cat .gitignore | grep .env

# Agar yo'q bo'lsa:
echo ".env" >> .gitignore
```

### Bot tokenini server environment variable sifatida saqlash

---

## ✅ Tekshirish

1. Bot ishga tushdi:
   - Telegram da `/start` kommandasini yuboring
   - Banner ko'rinishi kerak

2. Video qismlari ishlaydi:
   - `/list` → raqam (8, 14, 15...)
   - Video kelishi kerak

3. 24/7 ishlaydi:
   - Serverda `systemctl status filmbot`
   - Yoki Railway/Render dashboard

---

## 🆘 Muammolar

### Bot ishga tushmaydi:
```bash
# Loglarni tekshiring
sudo journalctl -u filmbot -f
```

### Video jo'natilmaydi:
- Fayl yo'li to'g'ri ekanini tekshiring
- Fayl hajmi 50MB dan kichik bo'lishi kerak

### "Conflict" xatosi:
- Bir vaqtning o'zida 2 ta bot instance ishlamoqda
- Bittasini to'xtating

---

## 📞 Yordam

Agar muammo bo'lsa:
1. Loglarni ko'ring
2. `.env` fayl to'g'ri ekanini tekshiring
3. Internet bog'lanishni tekshiring

**Omad!** 🚀
