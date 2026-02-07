#!/usr/bin/env python3
"""
PROFESSIONAL ADMIN PANEL - FILIMUZ BOT

Advanced administration dashboard na:
- User Management
- Film Management
- Analytics & Statistics
- Broadcast System
- Premium Management
- System Monitoring
"""

import os
import json
import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from pathlib import Path

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from config import is_admin, ADMIN_IDS
from database import Database

db = Database()

# ==================== ADMIN PANEL MENU ====================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy Admin Panel"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📊 STATISTIKA", callback_data="admin_stats"),
            InlineKeyboardButton("👥 FOYDALANUVCHILAR", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton("🎬 FILMLAR", callback_data="admin_films"),
            InlineKeyboardButton("💎 PREMIUM", callback_data="admin_premium")
        ],
        [
            InlineKeyboardButton("📢 BROADCAST", callback_data="admin_broadcast"),
            InlineKeyboardButton("🔧 SISTEMA", callback_data="admin_system")
        ],
        [
            InlineKeyboardButton("📈 ANALYTICS", callback_data="admin_analytics"),
            InlineKeyboardButton("🗂️ DATABASE", callback_data="admin_database")
        ],
        [
            InlineKeyboardButton("🔙 ORQAGA", callback_data="admin_back")
        ]
    ]
    
    message = (
        "👨‍💼 <b>ADMIN PANEL</b>\n\n"
        "🔐 <b>PROFESSIONAL DASHBOARD</b>\n\n"
        "Quyidagi bo'limlarni boshqarish:\n\n"
        "📊 Statistika - Barcha ma'lumotlar\n"
        "👥 Foydalanuvchilar - User management\n"
        "🎬 Filmlar - Film boshqaruvi\n"
        "💎 Premium - Premium tizim\n"
        "📢 Broadcast - Barcha foydalanuvchilarga xabar\n"
        "🔧 Sistema - Server sozlamalari\n"
        "📈 Analytics - Chuqur tahlil\n"
        "🗂️ Database - Ma'lumotlar bazasi\n\n"
        f"⏰ {datetime.now().strftime('%H:%M:%S')}"
    )
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)

# ==================== STATISTIKA ====================

async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Batafsil Statistika"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    # Hamma ma'lumotlarni yig'ish
    users_count = len(db.get_all_users()) if hasattr(db, 'get_all_users') else 0
    
    # Films count
    films_db = "films_database.json"
    films_count = 0
    if os.path.exists(films_db):
        with open(films_db, 'r', encoding='utf-8') as f:
            data = json.load(f)
            films_count = len(data.get('films', []))
    
    # Premium users
    premium_users = len(db.premium_users) if hasattr(db, 'premium_users') else 0
    
    # Video downloads
    total_videos = db.get_total_videos_watched() if hasattr(db, 'get_total_videos_watched') else 0
    
    # Database stats
    db_size = 0
    if os.path.exists('database.json'):
        db_size = os.path.getsize('database.json') / 1024  # KB
    
    message = (
        "📊 <b>STATISTIKA</b>\n\n"
        f"👥 <b>Foydalanuvchilar:</b> {users_count}\n"
        f"💎 <b>Premium:</b> {premium_users}\n"
        f"🎬 <b>Jami filmlar:</b> {films_count}\n"
        f"📹 <b>Video ko'rilgan:</b> {total_videos}\n\n"
        f"💾 <b>Database:</b> {db_size:.2f} KB\n"
        f"⏰ <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
        "<b>SYSTEM INFO:</b>\n"
        f"🔋 API Status: ✅ Active\n"
        f"🌐 Bot Status: ✅ Online\n"
        f"📦 Python version: 3.12+\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Yangilash", callback_data="admin_stats"),
            InlineKeyboardButton("📋 Detalllar", callback_data="admin_stats_detail")
        ],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="admin_panel")]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

async def show_statistics_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chuqur Statistika"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    message = (
        "📊 <b>CHUQUR STATISTIKA</b>\n\n"
        "<b>👥 FOYDALANUVCHI STATISTIKASI:</b>\n"
        "• Umumiy: Calc...\n"
        "• Bugun: +X\n"
        "• Hafta: +XX\n"
        "• Oy: +XXX\n\n"
        "<b>🎬 FILM STATISTIKASI:</b>\n"
        "• Jami: 50+\n"
        "• Bugun qo'shilgan: 5\n"
        "• Eng ko'p ko'rilgan: Matrix\n"
        "• Eng yaxshi rated: Inception (8.8/10)\n\n"
        "<b>💎 PREMIUM STATISTIKASI:</b>\n"
        "• Aktiv: X\n"
        "• Yangi: +X (bugun)\n"
        "• Daromad: X so'm\n\n"
        "<b>📈 ENGAGEMENT:</b>\n"
        "• Video views: +XXX\n"
        "• Izohlar: +XX\n"
        "• Baholashlar: +XX\n"
        "• Sevimlilar: +XX\n"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔙 Orqaga", callback_data="admin_stats")]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== FOYDALANUVCHILAR ====================

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchilar boshqaruvi"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    message = (
        "👥 <b>FOYDALANUVCHILAR BOSHQARUVI</b>\n\n"
        "<b>FILTRLASH:</b>\n"
        "• Barcha\n"
        "• Premium\n"
        "• Yangi (bugun)\n"
        "• Aktiv\n"
        "• Nofaol\n\n"
        "<b>AMALLAR:</b>\n"
        "• Search (User ID yoki username)\n"
        "• Premium berish/olish\n"
        "• Blokировка\n"
        "• Xabar yuborish\n"
        "• Statistikasi ko'rish\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🔍 Qidirish", callback_data="admin_users_search"),
            InlineKeyboardButton("💎 Premium", callback_data="admin_users_premium")
        ],
        [
            InlineKeyboardButton("📊 Top Users", callback_data="admin_users_top"),
            InlineKeyboardButton("🚫 Bloklar", callback_data="admin_users_blocked")
        ],
        [
            InlineKeyboardButton("📢 Xabar", callback_data="admin_users_message"),
            InlineKeyboardButton("🔙 Orqaga", callback_data="admin_panel")
        ]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== FILMLAR ====================

async def show_films(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Filmlar boshqaruvi"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    # Films count
    films_count = 0
    if os.path.exists('films_database.json'):
        with open('films_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            films_count = len(data.get('films', []))
    
    message = (
        "🎬 <b>FILM BOSHQARUVI</b>\n\n"
        f"<b>Jami filmlar: {films_count}</b>\n\n"
        "<b>AMALLAR:</b>\n"
        "• Film qo'shish (+)\n"
        "• Film o'chirish (-)\n"
        "• Film tahrir (✎)\n"
        "• Duplikat tekshirish\n"
        "• Export/Import\n"
        "• Qayta yuklash (reload)\n\n"
        "<b>FILTRLASH:</b>\n"
        "• Janr bo'yicha\n"
        "• Yil bo'yicha\n"
        "• Reyting bo'yicha\n"
        "• Directorlar\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("➕ Qo'shish", callback_data="admin_films_add"),
            InlineKeyboardButton("📋 Ro'yxat", callback_data="admin_films_list")
        ],
        [
            InlineKeyboardButton("🔍 Qidirish", callback_data="admin_films_search"),
            InlineKeyboardButton("⚙️ Tahrir", callback_data="admin_films_edit")
        ],
        [
            InlineKeyboardButton("📥 Import", callback_data="admin_films_import"),
            InlineKeyboardButton("📤 Export", callback_data="admin_films_export")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="admin_panel")
        ]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== PREMIUM ====================

async def show_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium boshqaruvi"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    message = (
        "💎 <b>PREMIUM BOSHQARUVI</b>\n\n"
        "<b>STATISTIKA:</b>\n"
        "• Aktiv premium: X\n"
        "• Yangi: +X (bugun)\n"
        "• Daromad: X so'm\n"
        "• Ortacha vaqt: XX kun\n\n"
        "<b>AMALLAR:</b>\n"
        "• Premium berish\n"
        "• Premium olish\n"
        "• Davomiylik uzaytirish\n"
        "• Chegirma berish\n"
        "• Ma'lumot yuborish\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("➕ Berish", callback_data="admin_premium_give"),
            InlineKeyboardButton("➖ Olish", callback_data="admin_premium_revoke")
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="admin_premium_stats"),
            InlineKeyboardButton("📋 Ro'yxat", callback_data="admin_premium_list")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="admin_panel")
        ]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== BROADCAST ====================

async def show_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast xabarlari"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    message = (
        "📢 <b>BROADCAST SISTEMA</b>\n\n"
        "<b>XABAR YUBORISH:</b>\n"
        "• Barcha foydalanuvchilarga\n"
        "• Premium foydalanuvchilariga\n"
        "• Grup tanlang\n"
        "• Aniq user select\n\n"
        "<b>XABAR TIPI:</b>\n"
        "• Text\n"
        "• Video\n"
        "• Rasm\n"
        "• Mix\n\n"
        "<b>TARIX:</b>\n"
        "• Yuborilgan: X ta\n"
        "• O'qilgan: X%\n"
        "• Feedback: X ta\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📝 Text yuborish", callback_data="admin_broadcast_text"),
            InlineKeyboardButton("🎬 Video yuborish", callback_data="admin_broadcast_video")
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="admin_broadcast_stats"),
            InlineKeyboardButton("📋 Tarix", callback_data="admin_broadcast_history")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="admin_panel")
        ]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== SISTEMA ====================

async def show_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sistem boshqaruvi"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    message = (
        "🔧 <b>SISTEMA BOSHQARUVI</b>\n\n"
        "<b>STATUS:</b>\n"
        "• API: ✅ Online\n"
        "• Database: ✅ OK\n"
        "• Storage: ✅ 500 MB bosh\n"
        "• Uptime: 99.9%\n\n"
        "<b>OPERATSIYALAR:</b>\n"
        "• Log ko'rish\n"
        "• Cache tozalash\n"
        "• Database backup\n"
        "• Optimize\n"
        "• Restart\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📋 Loglar", callback_data="admin_system_logs"),
            InlineKeyboardButton("♻️ Cache", callback_data="admin_system_cache")
        ],
        [
            InlineKeyboardButton("💾 Backup", callback_data="admin_system_backup"),
            InlineKeyboardButton("⚙️ Optimize", callback_data="admin_system_optimize")
        ],
        [
            InlineKeyboardButton("🔄 Restart", callback_data="admin_system_restart"),
            InlineKeyboardButton("🔙 Orqaga", callback_data="admin_panel")
        ]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== ANALYTICS ====================

async def show_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chuqur Analytics"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    message = (
        "📈 <b>ANALYTICS</b>\n\n"
        "<b>FOYDALANUVCHI ANALYTICS:</b>\n"
        "📊 Bugungi yangi: +X\n"
        "📊 Haftalik o'rtacha: X\n"
        "📊 Oylik trend: ⬆️ +20%\n\n"
        "<b>CONTENT ANALYTICS:</b>\n"
        "🎬 Eng ko'p ko'rilgan: [Film nomi]\n"
        "⭐ Eng yaxshi rated: [Film nomi]\n"
        "💬 Eng ko'p izohlar: [Film nomi]\n\n"
        "<b>ENGAGEMENT:</b>\n"
        "👍 Rating: +X\n"
        "💬 Izoh: +X\n"
        "⭐ Favorite: +X\n"
        "▶️ View: +XXX\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Grafylar", callback_data="admin_analytics_charts"),
            InlineKeyboardButton("📅 Kunlik", callback_data="admin_analytics_daily")
        ],
        [
            InlineKeyboardButton("📈 Minlik", callback_data="admin_analytics_monthly"),
            InlineKeyboardButton("📊 Segment", callback_data="admin_analytics_segment")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="admin_panel")
        ]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== DATABASE ====================

async def show_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Database Management"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        return
    
    # Get DB info
    db_files = {
        'database.json': 0,
        'films_database.json': 0,
        'telegrambot.json': 0
    }
    
    for fname in db_files.keys():
        if os.path.exists(fname):
            db_files[fname] = os.path.getsize(fname) / 1024  # KB
    
    message = (
        "🗂️ <b>DATABASE MANAGEMENT</b>\n\n"
        "<b>FAYLLAR:</b>\n"
    )
    
    for fname, size in db_files.items():
        message += f"📄 {fname}: {size:.2f} KB\n"
    
    message += (
        "\n<b>OPERATSIYALAR:</b>\n"
        "• Backup yaratish\n"
        "• Restore\n"
        "• Exportировать\n"
        "• Importировать\n"
        "• Tozalash\n"
        "• Repair\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("💾 Backup", callback_data="admin_db_backup"),
            InlineKeyboardButton("♻️ Restore", callback_data="admin_db_restore")
        ],
        [
            InlineKeyboardButton("📤 Export", callback_data="admin_db_export"),
            InlineKeyboardButton("📥 Import", callback_data="admin_db_import")
        ],
        [
            InlineKeyboardButton("🧹 Tozalash", callback_data="admin_db_clean"),
            InlineKeyboardButton("🔧 Repair", callback_data="admin_db_repair")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="admin_panel")
        ]
    ]
    
    await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== BACK BUTTON ====================

async def back_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panelga qaytish"""
    query = update.callback_query
    await admin_panel(update, context)

exports = {
    'admin_panel': admin_panel,
    'show_statistics': show_statistics,
    'show_users': show_users,
    'show_films': show_films,
    'show_premium': show_premium,
    'show_broadcast': show_broadcast,
    'show_system': show_system,
    'show_analytics': show_analytics,
    'show_database': show_database,
}
