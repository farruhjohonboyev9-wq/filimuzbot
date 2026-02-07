#!/bin/bash

# Filimuz Bot - Deployment Validation Script
# Server ga joylashtirishdagi muammolarni tekshirish

echo "🔍 Filimuz Bot Deployment Validation"
echo "======================================"
echo ""

# 1. Python tekshirish
echo "1️⃣ Python versiyasi tekshirilmoqda..."
if command -v python3.12 &> /dev/null; then
    echo "✅ Python 3.12 topildi: $(python3.12 --version)"
elif command -v python3 &> /dev/null; then
    echo "⚠️ Python 3.12 yo'q, lekin Python 3 bor: $(python3 --version)"
else
    echo "❌ Python topilmadi!"
fi
echo ""

# 2. Virtual environment tekshirish
echo "2️⃣ Virtual environment tekshirilmoqda..."
if [ -d "venv" ]; then
    echo "✅ Virtual environment mozjud"
else
    echo "⚠️ Virtual environment topilmadi, yarating:"
    echo "   python3.12 -m venv venv"
fi
echo ""

# 3. Requirements faylini tekshirish
echo "3️⃣ Requirements faylini tekshirilmoqda..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt topildi"
    echo "Paketlar:"
    cat requirements.txt | grep -v "^#" | grep -v "^$"
else
    echo "❌ requirements.txt topilmadi!"
fi
echo ""

# 4. .env tekshirish
echo "4️⃣ .env faylini tekshirilmoqda..."
if [ -f ".env" ]; then
    echo "✅ .env topildi"
    if grep -q "TELEGRAM_BOT_TOKEN" .env; then
        echo "✅ TELEGRAM_BOT_TOKEN o'rnatilgan"
    else
        echo "❌ TELEGRAM_BOT_TOKEN topilmadi"
    fi
    if grep -q "ADMIN_IDS" .env; then
        echo "✅ ADMIN_IDS o'rnatilgan"
    else
        echo "⚠️ ADMIN_IDS topilmadi"
    fi
else
    echo "❌ .env topilmadi! Yarating: nano .env"
fi
echo ""

# 5. Asosiy fayllarni tekshirish
echo "5️⃣ Asosiy fayllar tekshirilmoqda..."
FILES=("filimuz.py" "config.py" "database.py" "database.json" "films_database.json")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file topildi"
    else
        echo "⚠️ $file topilmadi"
    fi
done
echo ""

# 6. Port tekshirish
echo "6️⃣ Portlar tekshirilmoqda..."
if command -v lsof &> /dev/null; then
    if lsof -i :5000 &> /dev/null; then
        echo "⚠️ Port 5000 band. Bot yangi port ishlataishi mumkin."
    else
        echo "✅ Port 5000 bo'sh"
    fi
else
    echo "⚠️ lsof topilmadi"
fi
echo ""

# 7. Disk joy tekshirish
echo "7️⃣ Disk joy tekshirilmoqda..."
DISK_USAGE=$(df . | awk 'NR==2 {print int($5)}')
echo "Disk ishlatilish: ${DISK_USAGE}%"
if [ $DISK_USAGE -gt 90 ]; then
    echo "⚠️ Disk to'liqroq boyib ketmoqda!"
else
    echo "✅ Disk joy yetarli"
fi
echo ""

echo "======================================"
echo "✨ Tekshirish tugadi!"
echo ""
echo "Keyingi qadam: systemctl start filimuz"
