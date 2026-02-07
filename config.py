import os
import json
from dotenv import load_dotenv

load_dotenv()

# Admin ID lar (o'zingizning Telegram ID ni qo'shing)
# ID ni olish: @userinfobot ga /start yuboring
ADMIN_IDS = [
    # 123456789,  # 👈 O'zingizning Telegram ID ni qo'ying
]

# .env dan o'qish
admin_ids_env = os.getenv("ADMIN_IDS", "")
if admin_ids_env:
    ADMIN_IDS.extend([int(x.strip()) for x in admin_ids_env.split(",") if x.strip()])

def _load_admin_ids_from_db(db_file="database.json"):
    """Database faylidan admin ID larni olish"""
    if not os.path.exists(db_file):
        return []
    try:
        with open(db_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        raw_ids = data.get("admin_ids", [])
        return [int(x) for x in raw_ids if str(x).isdigit()]
    except Exception:
        return []

_DYNAMIC_ADMIN_IDS = _load_admin_ids_from_db()

def refresh_admin_ids():
    """Admin ID cache ni yangilash"""
    global _DYNAMIC_ADMIN_IDS
    _DYNAMIC_ADMIN_IDS = _load_admin_ids_from_db()
    return _DYNAMIC_ADMIN_IDS

def is_admin(user_id):
    """Foydalanuvchi admin ekanini tekshirish"""
    return user_id in ADMIN_IDS or user_id in _DYNAMIC_ADMIN_IDS
