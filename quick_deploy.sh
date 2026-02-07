#!/bin/bash

# Filimuz Bot - TEZKOR O'RNATISH SKRIPTI
# Bitta komanda bilan serverga o'rnatish

set -e  # Xatoga duch kelsa to'xtash

echo "🤖 FILIMUZ BOT - TEZKOR SERVER O'RNATISH"
echo "=========================================="
echo ""

# Rang kodlari
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Tizimni yangilash
echo -e "${YELLOW}1. Tizim yangilanmoqda...${NC}"
apt update && apt upgrade -y > /dev/null 2>&1
echo -e "${GREEN}✅ Tizim yangilandi${NC}"
echo ""

# 2. Python o'rnatish
echo -e "${YELLOW}2. Python 3.12 o'rnatilmoqda...${NC}"
if ! command -v python3.12 &> /dev/null; then
    apt install -y python3.12 python3.12-venv python3-pip > /dev/null 2>&1
fi
echo -e "${GREEN}✅ Python tayyor: $(python3.12 --version)${NC}"
echo ""

# 3. Git va tools
echo -e "${YELLOW}3. Kerakli tools o'rnatilmoqda...${NC}"
apt install -y git curl wget nano htop > /dev/null 2>&1
echo -e "${GREEN}✅ Tools o'rnatildi${NC}"
echo ""

# 4. Bot direktoriyasi
echo -e "${YELLOW}4. Bot direktoriyasi tayyorlanmoqda...${NC}"
if [ ! -d "/root/filimuz" ]; then
    echo "Direktoriya yo'q. /root dan o'ching:"
    echo "cd /root && git clone YOUR_REPO_URL filimuz"
    exit 1
fi
cd /root/filimuz
echo -e "${GREEN}✅ Direktoriya: /root/filimuz${NC}"
echo ""

# 5. Virtual environment
echo -e "${YELLOW}5. Virtual environment yaranmoqda...${NC}"
if [ ! -d "venv" ]; then
    python3.12 -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment faol${NC}"
echo ""

# 6. Requirements
echo -e "${YELLOW}6. Python paketlari o'rnatilmoqda...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✅ Barcha paketlar o'rnatildi${NC}"
echo ""

# 7. .env tekshirish
echo -e "${YELLOW}7. .env faylini tekshirilmoqda...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env faylini yarating!${NC}"
    echo "Quyidagini bajarang:"
    echo "  nano /root/filimuz/.env"
    echo ""
    echo "Va quyidagilarni kiriting:"
    echo "  TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN"
    echo "  ADMIN_IDS=YOUR_ADMIN_ID"
    exit 1
fi
echo -e "${GREEN}✅ .env tayyor${NC}"
echo ""

# 8. Systemd service
echo -e "${YELLOW}8. Systemd xizmati o'rnatilmoqda...${NC}"
cp /root/filimuz/filimuz.service /etc/systemd/system/filimuz.service
systemctl daemon-reload
systemctl enable filimuz
echo -e "${GREEN}✅ Systemd service o'rnatildi${NC}"
echo ""

# 9. Bot ishga tushmasi
echo -e "${YELLOW}9. Bot ishga tushmasi...${NC}"
systemctl start filimuz
sleep 2
if systemctl is-active --quiet filimuz; then
    echo -e "${GREEN}✅ Bot faol va ishlayapti!${NC}"
else
    echo -e "${RED}❌ Bot ishlamayapti. Loglarni tekshiring:${NC}"
    echo "   journalctl -u filimuz -n 50"
fi
echo ""

# 10. Status ko'rsatish
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ O'RNATISH TUGADI!${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "📊 Bot Status:"
systemctl status filimuz --no-pager
echo ""
echo "📝 Kerakli komandalar:"
echo "  - Statusni ko'rish: systemctl status filimuz"
echo "  - Loglarni ko'rish: journalctl -u filimuz -f"
echo "  - Botni qayta tushirish: systemctl restart filimuz"
echo "  - Botni to'xtatish: systemctl stop filimuz"
echo ""
