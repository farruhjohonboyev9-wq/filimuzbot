#!/bin/bash
# Video fayllarni siqish va tayyorlash skripti

echo "🎬 VIDEO TAYYORLASH SKRIPTI"
echo ""

# 1. ODDIY SIQISH (800KB/s)
echo "1️⃣ ODDIY SIQISH (800KB/s):"
echo "   ffmpeg -i input.mp4 -vcodec h264 -acodec aac -b:v 800k output.mp4"
echo ""

# 2. SIFATNI SAQLAGAN HOLDA SIQISH
echo "2️⃣ SIFATNI SAQLAGAN HOLDA (CRF 28):"
echo "   ffmpeg -i input.mp4 -vcodec h264 -crf 28 -preset slow output.mp4"
echo ""

# 3. TELEGRAM UCHUN OPTIMAL
echo "3️⃣ TELEGRAM UCHUN OPTIMAL (480p, 800kb/s):"
echo "   ffmpeg -i input.mp4 -vf scale=-2:480 -vcodec h264 -b:v 800k -maxrate 800k -bufsize 1600k -acodec aac -b:a 128k output.mp4"
echo ""

# 4. VIDEO KESISH
echo "4️⃣ VIDEO KESISH (5:00 dan 10:00 gacha):"
echo "   ffmpeg -i input.mp4 -ss 00:05:00 -to 00:10:00 -c copy output.mp4"
echo ""

# 5. VIDEO HAJMINI TEKSHIRISH
echo "5️⃣ VIDEO HAJMINI TEKSHIRISH:"
echo "   Fayl hajmi: ls -lh input.mp4"
echo "   yoki: du -h input.mp4"
echo ""

# 6. JUDA KICHIK HAJM (25MB)
echo "6️⃣ JUDA KICHIK HAJM (360p, 500kb/s - 25MB gacha):"
echo "   ffmpeg -i input.mp4 -vf scale=-2:360 -vcodec h264 -b:v 500k -maxrate 500k -bufsize 1000k -acodec aac -b:a 96k output.mp4"
echo ""

# MISOL
echo "📚 MISOL:"
echo ""
echo "Agar sizda 'bigmovie.mp4' (200MB) bo'lsa:"
echo ""
echo "# Telegramga mos qilish (50MB dan kam):"
echo "ffmpeg -i bigmovie.mp4 -vf scale=-2:480 -vcodec h264 -b:v 600k -acodec aac -b:a 96k mymovie.mp4"
echo ""
echo "# Natija: mymovie.mp4 (taxminan 40-45MB)"
echo ""

# WINDOWS UCHUN
echo "💡 WINDOWS FOYDALANUVCHILAR:"
echo ""
echo "1. FFmpeg yuklab oling: https://ffmpeg.org/download.html"
echo "2. PowerShell yoki CMD da ishlatishingiz mumkin:"
echo "   ffmpeg.exe -i input.mp4 -vcodec h264 -b:v 800k output.mp4"
echo ""

# QO'SHIMCHA VOSITALAR
echo "🛠️ QO'SHIMCHA VOSITALAR:"
echo ""
echo "1. HandBrake (GUI): https://handbrake.fr/"
echo "   - Oson interfeys"
echo "   - Preset'lar bor"
echo "   - Windows/Mac/Linux"
echo ""
echo "2. Online Video Converter:"
echo "   - cloudconvert.com"
echo "   - online-convert.com"
echo "   - freeconvert.com"
echo ""

# TEZLIK VA SIFAT
echo "⚡ TEZLIK VS SIFAT:"
echo ""
echo "Tez (past sifat):  -preset ultrafast"
echo "O'rtacha:          -preset medium"
echo "Sekin (yuqori):    -preset slow"
echo ""

# CRF QIYMATLARI
echo "📊 CRF QIYMATLARI (sifat):"
echo ""
echo "18-22: Juda yuqori sifat (katta fayl)"
echo "23-28: Yaxshi sifat (tavsiya etiladi)"
echo "29-35: O'rtacha sifat (kichik fayl)"
echo ""

echo "✅ TAYYOR! Yuqoridagi buyruqlardan foydalaning"
