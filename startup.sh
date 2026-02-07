#!/bin/bash

# Filimuz Bot - Server Startup Script
# Ubuntu/Debian Linux uchun

echo "🤖 Filimuz Bot ishga tushmoqda..."

# Python virtual environment yaratish
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment yaranmoqda..."
    python3.12 -m venv venv || python3.11 -m venv venv || python3 -m venv venv
fi

# Virtual environment ni aktivlashtirish
source venv/bin/activate

# Requirements o'rnatish
echo "📥 Paketlar o'rnatilmoqda..."
pip install --upgrade pip
pip install -r requirements.txt

# .env tekshirish
if [ ! -f ".env" ]; then
    echo "⚠️ .env fayly topilmadi! Uni yarating:"
    echo "TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE"
    echo "ADMIN_IDS=YOUR_ADMIN_ID_HERE"
    exit 1
fi

# Bot ishga tushmasi
echo "✅ Bot ishga tushmoqda..."
python filimuz.py
