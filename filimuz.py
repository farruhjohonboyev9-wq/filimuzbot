from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
import random
import os
import json
import logging
import csv
from dotenv import load_dotenv
import yt_dlp
import asyncio
from pathlib import Path
from datetime import datetime
from uuid import uuid4

# .env fayldan o'qish
load_dotenv()

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database va Admin config import
from database import Database
from config import is_admin, ADMIN_IDS, refresh_admin_ids
from translations import get_text, format_text, TRANSLATIONS

# Database yaratish
db = Database()

# ==================== ADMIN ROLES & PERMISSIONS ====================

ADMIN_ROLES = ["SUPERADMIN", "ADMIN", "FILM_ADMIN", "BROADCASTER", "ANALYTICS"]

ROLE_PERMISSIONS = {
    "SUPERADMIN": {"admin_manage", "film_manage", "broadcast", "analytics"},
    "ADMIN": {"film_manage", "broadcast", "analytics"},
    "FILM_ADMIN": {"film_manage"},
    "BROADCASTER": {"broadcast"},
    "ANALYTICS": {"analytics"},
}

def get_admin_role(user_id):
    """Admin rolini olish (config adminlar SUPERADMIN)"""
    if user_id in ADMIN_IDS:
        return "SUPERADMIN"
    return db.get_admin_role(user_id) or "ADMIN"

def has_permission(user_id, perm):
    """Admin ruxsatini tekshirish"""
    if not is_admin(user_id):
        return False
    role = get_admin_role(user_id)
    return perm in ROLE_PERMISSIONS.get(role, set())

def log_admin_action(admin_id, action, target, status="SUCCESS", details=None):
    """Admin amalini audit logga yozish"""
    entry = {
        "admin_id": admin_id,
        "action": action,
        "target": target,
        "status": status,
        "details": details or {},
        "timestamp": datetime.now().isoformat()
    }
    try:
        log_file = "admin_audit.json"
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
        data.append(entry)
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

async def resolve_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """@username yoki ID dan chat ID olish"""
    if text.isdigit():
        return int(text)
    if text.startswith('@'):
        try:
            chat = await context.bot.get_chat(text)
            return chat.id
        except Exception:
            await update.message.reply_text("❌ Chat topilmadi")
            return None
    return None

async def send_scheduled_post(context: ContextTypes.DEFAULT_TYPE):
    """Job queue uchun scheduled post yuborish"""
    data = context.job.data or {}
    post_id = data.get("id")
    target = data.get("target")
    message_text = data.get("message")
    channel_id = data.get("channel_id")

    if target == "channel" and channel_id:
        try:
            await context.bot.send_message(chat_id=channel_id, text=message_text)
        except Exception:
            return
    else:
        user_ids = db.get_user_ids()
        for uid in user_ids:
            try:
                await context.bot.send_message(chat_id=uid, text=message_text)
            except Exception:
                pass
            await asyncio.sleep(0.05)

    if post_id:
        db.remove_scheduled_post(post_id)
        log_admin_action(data.get("admin_id", 0), "SCHEDULED_POST_SENT", str(target))

def schedule_pending_posts(app):
    """DB dagi scheduled postlarni qayta rejalashtirish"""
    posts = db.get_scheduled_posts()
    now = datetime.now()
    for post in posts:
        try:
            run_at = datetime.fromisoformat(post.get("run_at"))
        except Exception:
            continue
        if run_at <= now:
            continue
        delay = (run_at - now).total_seconds()
        app.job_queue.run_once(send_scheduled_post, delay, data=post)

# ==================== HELPER FUNCTIONS ====================

def get_film_keyboard(user_id, film_key, show_video=True):
    """Film uchun inline keyboard yaratish"""
    is_fav = db.is_favorite(user_id, film_key)
    user_rating = db.get_user_rating(user_id, film_key)
    
    buttons = []
    
    # 1-qator: Video va Sevimlilar
    row1 = []
    if show_video:
        row1.append(InlineKeyboardButton("▶️ Video", callback_data=f"watch_{film_key}"))
    
    if is_fav:
        row1.append(InlineKeyboardButton("❌ Sevimlilardan", callback_data=f"unfav_{film_key}"))
    else:
        row1.append(InlineKeyboardButton("⭐ Sevimlilar", callback_data=f"fav_{film_key}"))
    
    if row1:
        buttons.append(row1)
    
    # 2-qator: Baholash va Izohlar
    rate_text = f"⭐ Baholash ({user_rating})" if user_rating else "⭐ Baholash"
    buttons.append([
        InlineKeyboardButton(rate_text, callback_data=f"rate_{film_key}"),
        InlineKeyboardButton("💬 Izohlar", callback_data=f"comments_{film_key}")
    ])
    
    # 3-qator: Statistika
    avg_rating = db.get_average_rating(film_key)
    rating_count = db.get_rating_count(film_key)
    comment_count = db.get_comment_count(film_key)
    
    stats_text = f"📊 {avg_rating or 0:.1f}⭐ ({rating_count}) | 💬 {comment_count}"
    buttons.append([InlineKeyboardButton(stats_text, callback_data=f"stats_{film_key}")])
    
    return InlineKeyboardMarkup(buttons)

def format_film_info(film_key, film, user_id=None):
    """Film ma'lumotini formatlash"""
    message = f"📽️ <b>{film['title']}</b>\n"
    message += f"📅 Yil: {film['year']}\n"
    message += f"⭐ Reyting: {film['rating']}/10\n"
    
    # Foydalanuvchi baholari
    if user_id:
        avg_rating = db.get_average_rating(film_key)
        rating_count = db.get_rating_count(film_key)
        if avg_rating:
            message += f"👥 Jamoa bahosi: {avg_rating}⭐ ({rating_count} ta)\n"
    
    message += f"🎭 Janr: {film['janr']}\n"
    message += f"👤 Director: {film['director']}\n"
    message += f"📝 {film['description']}"
    
    return message

# ==================== FILMLARNI YUKLASH ====================

def load_films_from_json(json_file="films_database.json"):
    """JSON fayldan filmlarni yuklash"""
    try:
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                films_dict = {}
                for film in data.get('films', []):
                    key = film.pop('key')  # key ni olib tashlaymiz
                    films_dict[key] = film
                print(f"[INFO] {len(films_dict)} ta film JSON fayldan yuklandi")
                return films_dict
        else:
            print(f"[WARNING] {json_file} topilmadi, standart filmlar ishlatiladi")
            return {}
    except Exception as e:
        print(f"[ERROR] Filmlarni yuklashda xatolik: {e}")
        return {}

def save_file_id_to_json(film_key, file_id, json_file="films_database.json"):
    """File ID ni JSON faylga saqlash"""
    try:
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Film topish va file_id qo'shish
            for film in data.get('films', []):
                if film.get('key') == film_key:
                    film['file_id'] = file_id
                    break
            
            # Faylga yozish
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ File ID JSON'ga saqlandi: {film_key}")
            return True
        
    except Exception as e:
        logger.error(f"❌ File ID saqlashda xatolik: {e}")
        return False

def load_films_db(json_file="films_database.json"):
    """Film database faylini yuklash"""
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"films": []}

def save_films_db(data, json_file="films_database.json"):
    """Film database faylini saqlash"""
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Film bazasi - dasturlash tiliga qarab filtrlanadi
# Tillar: python, cpp, csharp, php, java, javascript

# JSON fayldan filmlarni yuklash
json_films = load_films_from_json()

# Standart filmlar (JSON faylda bo'lmasa)
movies = {
    "wednesday1": {
        "title": "Wednesday - 1-qism",
        "year": 2024,
        "rating": 8.5,
        "janr": "Horror, Comedy, Mystery",
        "director": "Tim Burton",
        "description": "Wednesday Addams serialining 2-mavsum 1-qismi",
        "languages": ["python", "javascript"],
        "video": "./movies/Uenzdey 2-1 480p (asilmedia.net).mp4"
    },
    "wednesday2": {
        "title": "Wednesday - 2-qism",
        "year": 2024,
        "rating": 8.5,
        "janr": "Horror, Comedy, Mystery",
        "director": "Tim Burton",
        "description": "Wednesday Addams serialining 2-mavsum 2-qismi",
        "languages": ["python", "javascript"],
        "video": "./movies/Uenzdey 2-2 480p (asilmedia.net).mp4"
    },
    "wednesday3": {
        "title": "Wednesday - 3-qism",
        "year": 2024,
        "rating": 8.5,
        "janr": "Horror, Comedy, Mystery",
        "director": "Tim Burton",
        "description": "Wednesday Addams serialining 2-mavsum 3-qismi",
        "languages": ["python", "javascript"],
        "video": "./movies/Uenzdey 2-3 480p (asilmedia.net).mp4"
    },
    "wednesday4": {
        "title": "Wednesday - 4-qism",
        "year": 2024,
        "rating": 8.5,
        "janr": "Horror, Comedy, Mystery",
        "director": "Tim Burton",
        "description": "Wednesday Addams serialining 2-mavsum 4-qismi",
        "languages": ["python", "javascript"],
        "video": "./movies/Uenzdey 2-4 480p (asilmedia.net).mp4"
    },
    "wednesday5": {
        "title": "Wednesday - 5-qism",
        "year": 2024,
        "rating": 8.5,
        "janr": "Horror, Comedy, Mystery",
        "director": "Tim Burton",
        "description": "Wednesday Addams serialining 2-mavsum 5-qismi",
        "languages": ["python", "javascript"],
        "video": "./movies/Uenzdey 2-5 480p (asilmedia.net).mp4"
    },
    "wednesday6": {
        "title": "Wednesday - 6-qism",
        "year": 2024,
        "rating": 8.5,
        "janr": "Horror, Comedy, Mystery",
        "director": "Tim Burton",
        "description": "Wednesday Addams serialining 2-mavsum 6-qismi",
        "languages": ["python", "javascript"],
        "video": "./movies/Uenzdey 2-6 480p (asilmedia.net).mp4"
    },
    "wednesday7": {
        "title": "Wednesday - 7-qism",
        "year": 2024,
        "rating": 8.5,
        "janr": "Horror, Comedy, Mystery",
        "director": "Tim Burton",
        "description": "Wednesday Addams serialining 2-mavsum 7-qismi",
        "languages": ["python", "javascript"],
        "video": "./movies/Uenzdey 2-7 480p (asilmedia.net).mp4"
    },
    "wednesday8": {
        "title": "Wednesday - 8-qism",
        "year": 2024,
        "rating": 8.5,
        "janr": "Horror, Comedy, Mystery",
        "director": "Tim Burton",
        "description": "Wednesday Addams serialining 2-mavsum 8-qismi",
        "languages": ["python", "javascript"],
        "video": "./movies/Uenzdey 2-8 480p (asilmedia.net).mp4"
    }
}

# JSON fayldagi filmlarni qo'shish
if json_films:
    movies.update(json_films)
    print(f"[INFO] Jami {len(movies)} ta film mavjud")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menu - 2 ta main button"""
    # Foydalanuvchini database ga qo'shish
    user = update.effective_user
    is_new = db.add_user(user.id, user.username, user.first_name)
    
    keyboard = [
        ["🎬 FILMLAR", "📥 VIDEO"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Banner rasmini yuborish
    banner_path = Path("./banner/photo_2026-02-06_20-04-27.jpg")
    
    welcome_text = ("🎬 <b>Tarjima Filimlar Telegram Botiga Xush Kelibsiz!</b>\n\n"
                   "Bu botda siz Instagram va YouTube videolarni yuklashingiz, "
                   "kod jonatib filim tomosha qilishingiz mumkin.\n\n"
                   "💡 Video link yuboring yoki raqam tanlang!\n\n"
                   "Quyidagi tugmalardan birini bosing:")
    
    if banner_path.exists():
        with open(banner_path, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=welcome_text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
    else:
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

async def films_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Filmlar submenu"""
    keyboard = [
        ["/list", "/top", "/random"],
        ["/kodli", "🎬 FILMLAR", "📥 VIDEO"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📽️ <b>FILMLAR MENUSI</b>\n\n"
        "Qaysi filmni qidirasiz?\n\n"
        "/list - Barcha filmlar\n"
        "/top - Eng yaxshi 5 ta\n"
        "/random - Tasodifiy film\n"
        "/kodli - Faqat kodli kinolar",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def video_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Video downloader submenu"""
    keyboard = [
        ["/ig"],
        ["🎬 FILMLAR", "📥 VIDEO"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📥 <b>VIDEO YUKLOVCHI</b>\n\n"
        "YouTube yoki Instagram videoni yuklang:\n\n"
        "<b>Usul 1:</b> /ig komandadan keyin link kiriting\n"
        "/ig https://youtube.com/watch?v=ABC\n"
        "/ig https://instagram.com/p/ABC\n\n"
        "<b>Usul 2:</b> Link ni oddiy xabar sifatida yuboring\n"
        "Masalan: https://youtube.com/watch?v=ABC\n\n"
        "Bot avtomatik ravishda videoni yuklab beradi!",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def list_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha filmlar ro'yxati"""
    db.increment_command(update.effective_user.id)
    
    message = "📋 <b>BARCHA FILMLAR:</b>\n\n"
    film_list = list(movies.items())
    for idx, (key, film) in enumerate(film_list, 1):
        message += f"<b>{idx}.</b> 📽️ <b>{film['title']}</b> ({film['year']})\n"
        message += f"   ⭐ {film['rating']}/10 | 🎭 {film['janr']}\n"
        message += f"   Director: {film['director']}\n\n"
    
    message += "\n💡 <b>FOYDALANISH:</b> Videoni ko'rish uchun raqamni yuboring!\n"
    message += "Masalan, <code>1</code> yatqanda <b>Inception</b> vidoesini olasiz."
    
    keyboard = [["🎬 FILMLAR", "📥 VIDEO"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)

async def top_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Eng yaxshi filmlar"""
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)[:5]
    message = "⭐ <b>TOP 5 FILMLAR:</b>\n\n"
    for idx, (key, film) in enumerate(sorted_movies, 1):
        message += f"{idx}. <b>{film['title']}</b>\n"
        message += f"   ⭐ {film['rating']}/10\n"
        message += f"   🎭 {film['janr']}\n\n"
    
    keyboard = [["🎬 FILMLAR", "📥 VIDEO"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)

async def random_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tasodifiy film tavsiyasi"""
    key, film = random.choice(list(movies.items()))
    message = f"🎲 <b>TASODIFIY FILM TAVSIYASI:</b>\n\n"
    message += f"📽️ <b>{film['title']}</b>\n"
    message += f"📅 Yil: {film['year']}\n"
    message += f"⭐ Reyting: {film['rating']}/10\n"
    message += f"🎭 Janr: {film['janr']}\n"
    message += f"👤 Director: {film['director']}\n"
    message += f"📝 {film['description']}"
    
    keyboard = [["🎬 FILMLAR", "📥 VIDEO"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)

async def code_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Faqat kodli kinolar"""
    message = "💻 <b>KODLI KINOLAR:</b>\n\n"
    code_films = [film for film in movies.values() if "Kodli" in film['janr']]
    for film in code_films:
        message += f"📽️ <b>{film['title']}</b>\n"
        message += f"   ⭐ {film['rating']}/10 | {film['janr']}\n"
        message += f"   {film['description']}\n\n"
    await update.message.reply_text(message, parse_mode='HTML')

async def filter_by_language(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str, lang_display: str):
    """Dasturlash tiliga qarab filmlarni filter qilish"""
    message = f"💻 <b>{lang_display} FILMLAR:</b>\n\n"
    filtered = [film for film in movies.values() if language in film.get('languages', [])]
    
    if not filtered:
        await update.message.reply_text(f"❌ {lang_display} uchun film topilmadi.")
        return
    
    for film in sorted(filtered, key=lambda x: x['rating'], reverse=True):
        message += f"📽️ <b>{film['title']}</b> ({film['year']})\n"
        message += f"   ⭐ {film['rating']}/10\n"
        message += f"   {film['description']}\n\n"
    await update.message.reply_text(message, parse_mode='HTML')

async def python_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Python filmlar"""
    await filter_by_language(update, context, "python", "PYTHON")

async def cpp_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """C++ filmlar"""
    await filter_by_language(update, context, "cpp", "C++")

async def csharp_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """C# filmlar"""
    await filter_by_language(update, context, "csharp", "C#")

async def php_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """PHP filmlar"""
    await filter_by_language(update, context, "php", "PHP")

async def java_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Java filmlar"""
    await filter_by_language(update, context, "java", "JAVA")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam"""
    message = (
        "🤖 <b>FILM BOTINING KOMANDALAR:</b>\n\n"
        "<b>ASOSIY:</b>\n"
        "/list - Barcha filmlar ro'yxati\n"
        "/top - Eng yaxshi 5 ta film\n"
        "/random - Tasodifiy film tavsiyasi\n"
        "/kodli - Faqat kodli kinolar\n\n"
        "<b>RAQAMLI TANLASH:</b>\n"
        "Film raqamini yuboring (masalan: <code>1</code>, <code>5</code>)\n"
        "Misol: /list buyrugi bilan raqamlangan filmlar ko'ring, keyin raqam yuboring\n\n"
        "<b>VIDEO YUKLOVCHI:</b>\n"
        "/ig https://youtube.com/... - YouTube video\n"
        "/ig https://instagram.com/... - Instagram video\n\n"
        "<b>QIDIRUV:</b>\n"
        "Film nomini yozishingiz ham mumkin! (masalan: inception)\n\n"
        "/help - Ushbu yordam"
    )
    await update.message.reply_text(message, parse_mode='HTML')

# ==================== ADMIN PANEL ====================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel - faqat adminlar uchun"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    keyboard = [
        ["/stats", "/users", "/toprated"],
        ["/mostwatched", "/leaderboard"],
        ["/broadcast", "/post"],
        ["/schedulepost", "/schedulepostchannel"],
        ["/givepremium", "/revokepremium"],
        ["/addadmin", "/removeadmin"],
        ["/listadmins", "/setrole"],
        ["/addfilm", "/editfilm"],
        ["/deletefilm", "/importfilms"],
        ["/setchannel", "/postchannel"],
        ["🎬 FILMLAR", "📥 VIDEO"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    stats = db.get_stats()
    
    message = (
        "👤 <b>ADMIN PANEL</b>\n\n"
        "<b>STATISTIKA:</b>\n"
        f"👥 Jami foydalanuvchilar: {stats['total_users']}\n"
        f"⚡ Jami buyruqlar: {stats['total_commands']}\n"
        f"🎬 Jami videolar: {stats['total_videos_sent']}\n"
        f"💎 Premium foydalanuvchilar: {len(db.data.get('premium_users', []))}\n\n"
        "<b>KOMANDALAR:</b>\n"
        "📊 /stats - Bot statistikasi\n"
        "👥 /users - Foydalanuvchilar\n"
        "🏆 /toprated - Top filmlar\n"
        "🔥 /mostwatched - Ko'p ko'rilganlar\n"
        "👑 /leaderboard - Top users\n"
        "📢 /broadcast - Xabar yuborish\n"
        "📝 /post - Post qo'shish (broadcast)\n"
        "⏰ /schedulepost - Postni rejalash\n"
        "⏰ /schedulepostchannel - Kanal post reja\n"
        "📝 /logs - Bot loglari\n\n"
        "<b>PREMIUM:</b>\n"
        "/givepremium [user_id] - Premium berish\n"
        "/revokepremium [user_id] - Premium olish\n\n"
        "<b>ADMIN:</b>\n"
        "/addadmin [user_id|@username] - Admin qo'shish\n"
        "/removeadmin [user_id] - Admin o'chirish\n"
        "/listadmins - Adminlar ro'yxati\n"
        "/setrole [user_id] [role] - Admin rol\n"
        "/addfilm [file_id] - Film qo'shish\n"
        "/editfilm - Film tahrir\n"
        "/deletefilm - Film o'chirish\n"
        "/importfilms - Film import\n"
        "/setchannel - Post kanali\n"
        "/postchannel - Kanalga post\n\n"
        "⚡ Admin huquqlari faol"
    )
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistika - faqat adminlar"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    stats = db.get_stats()
    users = db.get_all_users()
    
    # Oxirgi 24 soatda faol foydalanuvchilar
    from datetime import datetime, timedelta
    now = datetime.now()
    active_24h = 0
    
    for user_data in users.values():
        last_active = datetime.fromisoformat(user_data["last_active"])
        if (now - last_active).total_seconds() < 86400:  # 24 soat
            active_24h += 1
    
    message = (
        f"📊 <b>BOT STATISTIKASI</b>\n\n"
        f"👥 <b>Foydalanuvchilar:</b> {stats['total_users']}\n"
        f"📈 <b>Oxirgi 24 soat:</b> {active_24h} ta faol\n"
        f"⚡ <b>Buyruqlar:</b> {stats['total_commands']}\n"
        f"🎬 <b>Videolar:</b> {stats['total_videos_sent']}\n"
        f"🎭 <b>Filmlar:</b> {len(movies)} ta\n\n"
        f"🚀 <b>Ishga tushgan:</b> {stats['bot_started'][:10]}"
    )
    
    await update.message.reply_text(message, parse_mode='HTML')

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchilar ro'yxati - faqat adminlar"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    users = db.get_all_users()
    
    if not users:
        await update.message.reply_text("📋 Foydalanuvchilar yo'q")
        return
    
    # Top 20 ta foydalanuvchini ko'rsatish
    sorted_users = sorted(
        users.values(), 
        key=lambda x: x['commands_used'], 
        reverse=True
    )[:20]
    
    message = f"👥 <b>FOYDALANUVCHILAR ({len(users)} ta)</b>\n\n"
    
    for idx, user in enumerate(sorted_users, 1):
        username = f"@{user['username']}" if user['username'] else user['first_name']
        message += (
            f"{idx}. {username}\n"
            f"   💬 {user['commands_used']} buyruq | "
            f"🎬 {user['videos_watched']} video\n"
        )
    
    if len(users) > 20:
        message += f"\n... va yana {len(users) - 20} ta"
    
    await update.message.reply_text(message, parse_mode='HTML')

async def _resolve_user_id_from_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """User ID yoki @username dan ID topish"""
    chat_id = await resolve_chat_id(update, context, text)
    if chat_id is None:
        await update.message.reply_text("❌ Username topilmadi yoki ochiq emas")
    return chat_id

async def addadmin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin qo'shish - faqat adminlar"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "admin_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        context.user_data['pending_admin_add'] = True
        await update.message.reply_text(
            "🛡️ <b>ADMIN QO'SHISH</b>\n\n"
            "User ID yoki @username yuboring:\n"
            "Misol: <code>123456789</code> yoki <code>@username</code>\n\n"
            "Bekor qilish: /cancel",
            parse_mode='HTML'
        )
        return
    
    target_text = ' '.join(context.args).strip()
    target_id = await _resolve_user_id_from_text(update, context, target_text)
    if not target_id:
        return
    
    if target_id in ADMIN_IDS:
        await update.message.reply_text("ℹ️ Bu admin allaqachon config.py da mavjud")
        return
    
    if db.add_admin_id(target_id):
        db.set_admin_role(target_id, "ADMIN")
        refresh_admin_ids()
        await update.message.reply_text(
            f"✅ Admin qo'shildi: <code>{target_id}</code>",
            parse_mode='HTML'
        )
        log_admin_action(user_id, "ADD_ADMIN", str(target_id))
    else:
        await update.message.reply_text("ℹ️ Bu admin allaqachon ro'yxatda")

async def removeadmin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin o'chirish - faqat adminlar"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "admin_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        context.user_data['pending_admin_remove'] = True
        await update.message.reply_text(
            "🛡️ <b>ADMIN O'CHIRISH</b>\n\n"
            "User ID yuboring:\n"
            "Misol: <code>123456789</code>\n\n"
            "Bekor qilish: /cancel",
            parse_mode='HTML'
        )
        return
    
    target_text = ' '.join(context.args).strip()
    target_id = await _resolve_user_id_from_text(update, context, target_text)
    if not target_id:
        return
    
    if target_id in ADMIN_IDS:
        await update.message.reply_text("❌ Bu admin config.py dan o'chiriladi")
        return
    
    if db.remove_admin_id(target_id):
        refresh_admin_ids()
        await update.message.reply_text(
            f"✅ Admin o'chirildi: <code>{target_id}</code>",
            parse_mode='HTML'
        )
        log_admin_action(user_id, "REMOVE_ADMIN", str(target_id))
    else:
        await update.message.reply_text("ℹ️ Bu admin ro'yxatda yo'q")

async def listadmins_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adminlar ro'yxati"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "admin_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    static_admins = [str(x) for x in ADMIN_IDS]
    dynamic_admins = [str(x) for x in db.get_admin_ids()]
    
    message = "🛡️ <b>ADMINLAR RO'YXATI</b>\n\n"
    message += "<b>Config adminlar:</b>\n"
    message += "\n".join(static_admins) if static_admins else "(yo'q)"
    message += "\n\n<b>Qo'shilgan adminlar:</b>\n"
    message += "\n".join(dynamic_admins) if dynamic_admins else "(yo'q)"
    
    await update.message.reply_text(message, parse_mode='HTML')

async def setrole_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin rolini o'rnatish"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "admin_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if len(context.args) < 2:
        context.user_data['pending_setrole'] = True
        await update.message.reply_text(
            "🛡️ <b>ADMIN ROLI</b>\n\n"
            "Format:\n"
            "<code>UserID Role</code>\n\n"
            "Rolari: SUPERADMIN, ADMIN, FILM_ADMIN, BROADCASTER, ANALYTICS\n\n"
            "Misol: <code>123456789 FILM_ADMIN</code>\n"
            "Bekor: /cancel",
            parse_mode='HTML'
        )
        return
    
    target_text = context.args[0].strip()
    role = context.args[1].strip().upper()
    target_id = await _resolve_user_id_from_text(update, context, target_text)
    if not target_id:
        return
    
    if role not in ADMIN_ROLES:
        await update.message.reply_text("❌ Noto'g'ri rol")
        return
    
    if not is_admin(target_id):
        db.add_admin_id(target_id)
        refresh_admin_ids()
    db.set_admin_role(target_id, role)
    
    await update.message.reply_text(
        f"✅ Admin roli o'rnatildi: <code>{target_id}</code> -> <b>{role}</b>",
        parse_mode='HTML'
    )
    log_admin_action(user_id, "SET_ROLE", str(target_id), details={"role": role})

async def setchannel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Post kanalini sozlash"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "broadcast"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        context.user_data['pending_setchannel'] = True
        await update.message.reply_text(
            "📣 <b>POST KANALI</b>\n\n"
            "Kanal @username yoki ID yuboring.\n"
            "Misol: <code>@mychannel</code> yoki <code>-1001234567890</code>\n"
            "Bekor: /cancel",
            parse_mode='HTML'
        )
        return
    
    target_text = ' '.join(context.args).strip()
    channel_id = await resolve_chat_id(update, context, target_text)
    if channel_id is None:
        return
    
    db.set_setting("post_channel_id", channel_id)
    await update.message.reply_text(
        f"✅ Post kanali saqlandi: <code>{channel_id}</code>",
        parse_mode='HTML'
    )
    log_admin_action(user_id, "SET_CHANNEL", str(channel_id))

async def postchannel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanalga post yuborish"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "broadcast"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    channel_id = db.get_setting("post_channel_id")
    if not channel_id:
        await update.message.reply_text("❌ Post kanali o'rnatilmagan. /setchannel bering")
        return
    
    if not context.args:
        context.user_data['pending_postchannel'] = True
        await update.message.reply_text(
            "📝 <b>KANALGA POST</b>\n\n"
            "Xabar matnini yuboring.\n"
            "Bekor: /cancel",
            parse_mode='HTML'
        )
        return
    
    message_text = ' '.join(context.args)
    try:
        await context.bot.send_message(chat_id=channel_id, text=message_text)
        await update.message.reply_text("✅ Kanalga yuborildi")
        log_admin_action(user_id, "POST_CHANNEL", str(channel_id))
    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {str(e)[:80]}")

async def schedulepost_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Postni rejalash (hamma userlarga)"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "broadcast"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        context.user_data['pending_schedulepost'] = True
        await update.message.reply_text(
            "⏰ <b>POST REJALASH</b>\n\n"
            "Format:\n"
            "<code>YYYY-MM-DD HH:MM | Xabar</code>\n\n"
            "Misol:\n"
            "<code>2026-02-10 20:30 | Yangi filmlar qo'shildi!</code>\n"
            "Bekor: /cancel",
            parse_mode='HTML'
        )
        return
    
    raw = ' '.join(context.args)
    if '|' not in raw:
        await update.message.reply_text("❌ Format noto'g'ri")
        return
    time_text, message_text = [x.strip() for x in raw.split('|', 1)]
    try:
        run_at = datetime.strptime(time_text, "%Y-%m-%d %H:%M")
    except ValueError:
        await update.message.reply_text("❌ Sana format noto'g'ri")
        return
    
    if run_at <= datetime.now():
        await update.message.reply_text("❌ Vaqt kelajakda bo'lishi kerak")
        return
    
    post = {
        "id": uuid4().hex,
        "admin_id": user_id,
        "target": "all",
        "message": message_text,
        "run_at": run_at.isoformat()
    }
    db.add_scheduled_post(post)
    delay = (run_at - datetime.now()).total_seconds()
    context.application.job_queue.run_once(send_scheduled_post, delay, data=post)
    await update.message.reply_text("✅ Post rejalandi")
    log_admin_action(user_id, "SCHEDULE_POST", "all")

async def schedulepostchannel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Postni kanalga rejalash"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "broadcast"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    channel_id = db.get_setting("post_channel_id")
    if not channel_id:
        await update.message.reply_text("❌ Post kanali o'rnatilmagan. /setchannel bering")
        return
    
    if not context.args:
        context.user_data['pending_schedulepostchannel'] = True
        await update.message.reply_text(
            "⏰ <b>KANAL POST REJA</b>\n\n"
            "Format:\n"
            "<code>YYYY-MM-DD HH:MM | Xabar</code>\n\n"
            "Misol:\n"
            "<code>2026-02-10 20:30 | Kanalga post!</code>\n"
            "Bekor: /cancel",
            parse_mode='HTML'
        )
        return
    
    raw = ' '.join(context.args)
    if '|' not in raw:
        await update.message.reply_text("❌ Format noto'g'ri")
        return
    time_text, message_text = [x.strip() for x in raw.split('|', 1)]
    try:
        run_at = datetime.strptime(time_text, "%Y-%m-%d %H:%M")
    except ValueError:
        await update.message.reply_text("❌ Sana format noto'g'ri")
        return
    
    if run_at <= datetime.now():
        await update.message.reply_text("❌ Vaqt kelajakda bo'lishi kerak")
        return
    
    post = {
        "id": uuid4().hex,
        "admin_id": user_id,
        "target": "channel",
        "channel_id": channel_id,
        "message": message_text,
        "run_at": run_at.isoformat()
    }
    db.add_scheduled_post(post)
    delay = (run_at - datetime.now()).total_seconds()
    context.application.job_queue.run_once(send_scheduled_post, delay, data=post)
    await update.message.reply_text("✅ Kanal posti rejalandi")
    log_admin_action(user_id, "SCHEDULE_POST", str(channel_id))

async def editfilm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Film tahrir qilish"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "film_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        context.user_data['pending_editfilm'] = True
        await update.message.reply_text(
            "✏️ <b>FILM TAHRIR</b>\n\n"
            "Format:\n"
            "<code>key|field|value</code>\n\n"
            "Field: title, year, rating, janr, director, description, file_id, languages\n\n"
            "Misol:\n"
            "<code>inception|rating|9.0</code>\n"
            "Bekor: /cancel",
            parse_mode='HTML'
        )
        return
    
    raw = ' '.join(context.args)
    if '|' not in raw:
        await update.message.reply_text("❌ Format noto'g'ri")
        return
    key, field, value = [x.strip() for x in raw.split('|', 2)]
    
    data = load_films_db()
    films = data.get("films", [])
    film = next((f for f in films if f.get("key") == key), None)
    if not film:
        await update.message.reply_text("❌ Film topilmadi")
        return
    
    if field == "year":
        try:
            value = int(value)
        except ValueError:
            await update.message.reply_text("❌ Year raqam bo'lishi kerak")
            return
    elif field == "rating":
        try:
            value = float(value)
        except ValueError:
            await update.message.reply_text("❌ Rating raqam bo'lishi kerak")
            return
    elif field == "languages":
        value = [x.strip() for x in value.split(',') if x.strip()]
    
    if field not in ["title", "year", "rating", "janr", "director", "description", "file_id", "languages"]:
        await update.message.reply_text("❌ Field noto'g'ri")
        return
    
    film[field] = value
    save_films_db(data)
    await update.message.reply_text("✅ Film yangilandi")
    log_admin_action(user_id, "EDIT_FILM", key, details={"field": field})

    film_copy = film.copy()
    film_copy.pop('key', None)
    movies[key] = film_copy

async def deletefilm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Film o'chirish"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "film_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        context.user_data['pending_deletefilm'] = True
        await update.message.reply_text(
            "🗑️ <b>FILM O'CHIRISH</b>\n\n"
            "Film key yuboring.\n"
            "Misol: <code>inception</code>\n"
            "Bekor: /cancel",
            parse_mode='HTML'
        )
        return
    
    key = context.args[0].strip()
    data = load_films_db()
    films = data.get("films", [])
    before = len(films)
    films = [f for f in films if f.get("key") != key]
    if len(films) == before:
        await update.message.reply_text("❌ Film topilmadi")
        return
    data["films"] = films
    save_films_db(data)
    await update.message.reply_text("✅ Film o'chirildi")
    log_admin_action(user_id, "DELETE_FILM", key)

    if key in movies:
        del movies[key]

async def importfilms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Film import qilish"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "film_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    context.user_data['pending_importfilms'] = True
    await update.message.reply_text(
        "📥 <b>FILM IMPORT</b>\n\n"
        "JSON yoki CSV fayl yuboring.\n"
        "JSON format: {\"films\": [...]}\n"
        "CSV ustunlar: key,title,year,rating,janr,director,description,file_id,languages\n\n"
        "Bekor: /cancel",
        parse_mode='HTML'
    )

async def handle_import_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Film import hujjatini qayta ishlash"""
    user_id = update.effective_user.id
    
    if not context.user_data.get('pending_importfilms'):
        return
    if not has_permission(user_id, "film_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    doc = update.message.document
    if not doc:
        return
    
    file_name = doc.file_name or "import"
    ext = file_name.lower().split('.')[-1]
    if ext not in ["json", "csv"]:
        await update.message.reply_text("❌ Faqat JSON yoki CSV")
        return
    
    temp_dir = Path("./downloads")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / f"import_{uuid4().hex}.{ext}"
    
    try:
        file_obj = await context.bot.get_file(doc.file_id)
        await file_obj.download_to_drive(custom_path=str(temp_path))
        
        new_films = []
        if ext == "json":
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                new_films = data
            else:
                new_films = data.get("films", [])
        else:
            with open(temp_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    new_films.append(row)
        
        db_data = load_films_db()
        films = db_data.get("films", [])
        existing_keys = {f.get("key") for f in films}
        
        added = 0
        skipped = 0
        for film in new_films:
            key = str(film.get("key", "")).strip()
            title = str(film.get("title", "")).strip()
            year = film.get("year")
            rating = film.get("rating")
            janr = str(film.get("janr", "")).strip()
            director = str(film.get("director", "")).strip()
            description = str(film.get("description", "")).strip()
            if not all([key, title, year, rating, janr, director, description]):
                skipped += 1
                continue
            if key in existing_keys:
                skipped += 1
                continue
            try:
                year = int(year)
                rating = float(rating)
            except ValueError:
                skipped += 1
                continue
            languages = film.get("languages", ["python"])
            if isinstance(languages, str):
                languages = [x.strip() for x in languages.split(',') if x.strip()]
            file_id = film.get("file_id")
            films.append({
                "key": key,
                "title": title,
                "year": year,
                "rating": rating,
                "janr": janr,
                "director": director,
                "description": description,
                "languages": languages or ["python"],
                "file_id": file_id
            })
            existing_keys.add(key)
            added += 1
        
        db_data["films"] = films
        save_films_db(db_data)
        
        await update.message.reply_text(
            f"✅ Import yakunlandi!\nQo'shildi: {added}\nO'tkazib yuborildi: {skipped}"
        )
        log_admin_action(user_id, "IMPORT_FILMS", str(added), details={"skipped": skipped})

        # In-memory movies yangilash
        for film in films:
            key = film.get("key")
            if not key:
                continue
            film_copy = film.copy()
            film_copy.pop('key', None)
            movies[key] = film_copy
    except Exception as e:
        await update.message.reply_text(f"❌ Import xatosi: {str(e)[:100]}")
    finally:
        context.user_data.pop('pending_importfilms', None)
        try:
            if temp_path.exists():
                temp_path.unlink()
        except Exception:
            pass

async def _broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
    """Barcha foydalanuvchilarga xabar yuborish"""
    user_ids = db.get_user_ids()
    
    sent = 0
    failed = 0
    
    status_msg = await update.message.reply_text(
        f"📤 Xabar yuborilmoqda...\n0/{len(user_ids)}"
    )
    
    for idx, uid in enumerate(user_ids, 1):
        try:
            await context.bot.send_message(chat_id=uid, text=message_text)
            sent += 1
        except Exception:
            failed += 1
        
        if idx % 10 == 0:
            await status_msg.edit_text(
                f"📤 Yuborilmoqda...\n{idx}/{len(user_ids)}"
            )
        
        await asyncio.sleep(0.05)
    
    await status_msg.edit_text(
        f"✅ <b>POST YUBORILDI</b>\n\n"
        f"📨 Yuborildi: {sent}\n"
        f"❌ Xato: {failed}\n"
        f"📊 Jami: {len(user_ids)}",
        parse_mode='HTML'
    )

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Post qo'shish - barcha foydalanuvchilarga"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "broadcast"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        context.user_data['pending_post'] = True
        await update.message.reply_text(
            "📝 <b>POST QO'SHISH</b>\n\n"
            "Xabar matnini yuboring.\n"
            "Bekor qilish: /cancel",
            parse_mode='HTML'
        )
        return
    
    message_text = ' '.join(context.args)
    await _broadcast_message(update, context, message_text)
    log_admin_action(user_id, "POST_BROADCAST", "all")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha foydalanuvchilarga xabar yuborish"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "broadcast"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 <b>BROADCAST</b>\n\n"
            "Barcha foydalanuvchilarga xabar yuborish:\n"
            "/broadcast Sizning xabaringiz\n\n"
            "Misol:\n"
            "/broadcast Yangi filmlar qo'shildi!",
            parse_mode='HTML'
        )
        return
    
    message_text = ' '.join(context.args)
    user_ids = db.get_user_ids()
    
    sent = 0
    failed = 0
    
    status_msg = await update.message.reply_text(
        f"📤 Xabar yuborilmoqda...\n0/{len(user_ids)}"
    )
    
    for idx, uid in enumerate(user_ids, 1):
        try:
            await context.bot.send_message(chat_id=uid, text=message_text)
            sent += 1
        except Exception:
            failed += 1
        
        # Har 10 ta foydalanuvchidan keyin status yangilash
        if idx % 10 == 0:
            await status_msg.edit_text(
                f"📤 Yuborilmoqda...\n{idx}/{len(user_ids)}"
            )
        
        # Telegram flood limitini oldini olish
        await asyncio.sleep(0.05)  # 50ms
    
    await status_msg.edit_text(
        f"✅ <b>BROADCAST YAKUNLANDI</b>\n\n"
        f"📨 Yuborildi: {sent}\n"
        f"❌ Xato: {failed}\n"
        f"📊 Jami: {len(user_ids)}",
        parse_mode='HTML'
    )
    log_admin_action(user_id, "BROADCAST", "all", details={"sent": sent, "failed": failed})

async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot loglari - faqat adminlar"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    log_file = Path("bot.log")
    
    if log_file.exists():
        # Oxirgi 50 qator
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            last_lines = lines[-50:] if len(lines) > 50 else lines
            log_text = ''.join(last_lines)
        
        if len(log_text) > 4000:
            log_text = log_text[-4000:]
        
        await update.message.reply_text(
            f"📝 <b>BOT LOGLARI (oxirgi 50 qator)</b>\n\n"
            f"<code>{log_text}</code>",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text("📝 Log fayl topilmadi")

async def give_premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium berish - faqat adminlar"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        await update.message.reply_text(
            "💎 <b>PREMIUM BERISH</b>\n\n"
            "Foydalanish:\n"
            "/givepremium [user_id]\n\n"
            "Misol:\n"
            "/givepremium 123456789",
            parse_mode='HTML'
        )
        return
    
    try:
        target_user_id = int(context.args[0])
        db.set_premium(target_user_id, True)
        db.add_points(target_user_id, 100)  # Bonus 100 ball
        
        await update.message.reply_text(
            f"✅ <b>Premium berildi!</b>\n\n"
            f"👤 User ID: {target_user_id}\n"
            f"💎 Status: Premium\n"
            f"💰 Bonus: +100 ball",
            parse_mode='HTML'
        )
        
        # Foydalanuvchiga xabar yuborish
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="🎉 <b>Tabriklaymiz!</b>\n\n"
                     "💎 Sizga Premium status berildi!\n\n"
                     "<b>Xususiyatlar:</b>\n"
                     "✅ HD video yuklovchi\n"
                     "✅ Cheksiz sevimlilar\n"
                     "✅ Reklama yo'q\n"
                     "✅ Yangi filmlar birinchi bo'lib\n"
                     "✅ Shaxsiy tavsiyalar\n\n"
                     "💰 Bonus: +100 ball",
                parse_mode='HTML'
            )
        except:
            pass
        
    except ValueError:
        await update.message.reply_text("❌ Noto'g'ri user ID!")
    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {str(e)}")

async def revoke_premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium olish - faqat adminlar"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        await update.message.reply_text(
            "💎 <b>PREMIUM OLISH</b>\n\n"
            "Foydalanish:\n"
            "/revokepremium [user_id]\n\n"
            "Misol:\n"
            "/revokepremium 123456789",
            parse_mode='HTML'
        )
        return
    
    try:
        target_user_id = int(context.args[0])
        db.set_premium(target_user_id, False)
        
        await update.message.reply_text(
            f"✅ <b>Premium olindi!</b>\n\n"
            f"👤 User ID: {target_user_id}\n"
            f"🆓 Status: Oddiy",
            parse_mode='HTML'
        )
        
        # Foydalanuvchiga xabar yuborish
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="ℹ️ <b>Premium status tugadi</b>\n\n"
                     "Sizning Premium statusingiz tugadi.\n"
                     "Yangi Premium olish uchun /start buyrug'ini bosing.",
                parse_mode='HTML'
            )
        except:
            pass
        
    except ValueError:
        await update.message.reply_text("❌ Noto'g'ri user ID!")
    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {str(e)}")

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pending holatlarni bekor qilish"""
    keys = [
        'pending_admin_add',
        'pending_admin_remove',
        'pending_post',
        'pending_setrole',
        'pending_setchannel',
        'pending_postchannel',
        'pending_schedulepost',
        'pending_schedulepostchannel',
        'pending_editfilm',
        'pending_deletefilm',
        'pending_importfilms',
        'pending_file_id',
    ]
    for key in keys:
        context.user_data.pop(key, None)
    await update.message.reply_text("❌ Bekor qilindi")

async def addfilm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Film qo'shish - faqat adminlar"""
    user_id = update.effective_user.id
    
    if not has_permission(user_id, "film_manage"):
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🎬 <b>FILM QO'SHISH</b>\n\n"
            "Foydalanish:\n"
            "/addfilm [file_id]\n\n"
            "Misol:\n"
            "/addfilm BAACAgIAAxkDAAI...\n\n"
            "💡 File ID olish:\n"
            "1. Kanalga video yuklang\n"
            "2. <code>python get_file_id.py</code> ishga tushiring\n"
            "3. Bot'ga video'ni forward qiling\n"
            "4. File ID ni copy qiling",
            parse_mode='HTML'
        )
        return
    
    file_id = ' '.join(context.args).strip()
    
    # File ID ni saqlash
    context.user_data['pending_file_id'] = file_id
    
    await update.message.reply_text(
        "✅ <b>Film qo'shish boshlandi!</b>\n\n"
        "📝 Quyidagi formatda ma'lumotlarni yuboring:\n\n"
        "<code>Title|Year|Rating|Genre|Director|Description|Key</code>\n\n"
        "📋 <b>Misol:</b>\n"
        "<code>Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish haqida ajoyib film|inception</code>\n\n"
        "⚠️ Key - inglizcha, kichik harflar, probelsiz!",
        parse_mode='HTML'
    )

async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Video yuklovish - YouTube/Instagram"""
    
    if not context.args:
        await update.message.reply_text(
            "[VIDEO] Linkni kiriting:\n\n"
            "[YouTube] /ig https://youtube.com/watch?v=ABC\n"
            "[Instagram] /ig https://instagram.com/p/ABC\n\n"
            "MASLAHAT: YouTube video tavsiyalangan\n"
            "Qisqa video (Shorts) uchun: https://youtu.be/ABC"
        )
        return
    
    # URL extrakt qilish (message textdan kelib chiqqan bo'lsa, to'g'ri URL olish)
    url_text = context.args[0]
    
    # Agar butun message text bo'lsa, URL topish
    import re
    url_match = re.search(r'https?://[^\s]+', url_text)
    if url_match:
        url = url_match.group(0)
    else:
        url = url_text.strip()
    
    is_instagram = "instagram.com" in url
    is_youtube = "youtube.com" in url or "youtu.be" in url
    
    if not is_instagram and not is_youtube:
        await update.message.reply_text(
            "[ERROR] YouTube yoki Instagram kerak\n"
            "YouTube: https://youtube.com/watch?v=ABC\n"
            "Instagram: https://instagram.com/p/ABC"
        )
        return
    
    try:
        msg = await update.message.reply_text(
            f"[WAIT] Video yuklanmoqda...\n"
            f"[TYPE] {'YouTube' if is_youtube else 'Instagram'}\n"
            "[TIME] 1-3 minut kuting..."
        )
        
        downloads_dir = Path("./downloads")
        downloads_dir.mkdir(exist_ok=True)
        
        # Eski video o'chirish
        for old_file in downloads_dir.glob('*.mp4'):
            try:
                old_file.unlink()
            except:
                pass
        
        # yt-dlp sozlamalari
        ydl_opts = {
            'format': 'best[ext=mp4][height<=720]/best[height<=720]/best',
            'outtmpl': str(downloads_dir / 'video.mp4'),
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 60,
            'retries': 3,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            'geo_bypass': True,
            'skip_unavailable_fragments': True,
        }
        
        # YouTube format
        if is_youtube:
            ydl_opts['format'] = '18/22'  # YouTube default formats (360p/720p)
        
        # Video yukla
        def download_video():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return info
        
        loop = asyncio.get_event_loop()
        try:
            info = await asyncio.wait_for(
                loop.run_in_executor(None, download_video),
                timeout=180
            )
            video_title = info.get('title', 'Video')
        except asyncio.TimeoutError:
            await msg.edit_text("[ERROR] Vaqt tugadi (3 minut)")
            return
        except Exception as e:
            error_str = str(e).lower()
            
            # YouTube muammolar
            if is_youtube:
                if "unavailable" in error_str or "age" in error_str:
                    await msg.edit_text(
                        "[ERROR] Video ochiq emas yoki age-restricted\n"
                        "Boshqa YouTube linkini sinab ko'ring"
                    )
                elif "not found" in error_str or "404" in error_str:
                    await msg.edit_text("[ERROR] Video topilmadi")
                elif "geo" in error_str or "country" in error_str:
                    await msg.edit_text(
                        "[ERROR] Video sizning lokatsiyangizda mavjud emas"
                    )
                else:
                    await msg.edit_text(
                        f"[ERROR] YouTube: {str(e)[:80]}\n"
                        "Boshqa linkni sinab ko'ring"
                    )
            else:
                await msg.edit_text(
                    f"[ERROR] Instagram: {str(e)[:80]}"
                )
            return
        
        video_path = downloads_dir / "video.mp4"
        
        if not video_path.exists():
            await msg.edit_text(
                "[ERROR] Video saqlanmadi\n"
                "Qaytadan urinib ko'ring yoki boshqa link"
            )
            return
        
        file_size = video_path.stat().st_size
        
        if file_size > 50 * 1024 * 1024:
            video_path.unlink()
            await msg.edit_text(
                f"[ERROR] Video juda katta ({file_size / 1024 / 1024:.1f}MB)\n"
                "Maksimum: 50MB"
            )
            return
        
        # Videoni jo'natish
        await update.message.chat.send_action("upload_video")
        
        caption = f"[SUCCESS] Video: {video_title[:50]}"
        
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=caption
            )
        
        # Fayl o'chirish
        try:
            video_path.unlink()
        except:
            pass
        
    except Exception as e:
        await update.message.reply_text(
            f"[ERROR] Sistemali xato: {str(e)[:100]}"
        )

async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Raqam tashlasa film ma'lumoti va video yuborish"""
    text = update.message.text.strip()
    user_id = update.effective_user.id
    
    # Raqam tekshirish
    try:
        number = int(text)
    except ValueError:
        return False  # Bu raqam emas
    
    # Filmlarni list qilib olish
    film_list = list(movies.items())
    
    # Raqam diapazoni tekshirish (1 dan boshlanadi)
    if number < 1 or number > len(film_list):
        await update.message.reply_text(
            f"❌ {number} raqam mavjud emas!\n"
            f"📋 1-{len(film_list)} raqamlar orasidan tanlang\n\n"
            "/list - Raqamlangan filmlar ro'yxati"
        )
        return True
    
    # Filmni olish
    key, film = film_list[number - 1]
    
    # Film ma'lumotini yuborish (oddiy text)
    message = f"📽️ <b>{film['title']}</b>\n"
    message += f"📅 Yil: {film['year']}\n"
    message += f"⭐ Reyting: {film['rating']}/10\n"
    message += f"🎭 Janr: {film['janr']}\n"
    message += f"👤 Director: {film['director']}\n"
    message += f"📝 {film['description']}\n\n"
    message += "⏳ Video yuklanmoqda..."
    
    await update.message.reply_text(message, parse_mode='HTML')
    
    # Video yuborish
    caption = f"🎬 {film['title']} ({film['year']}) | ⭐ {film['rating']}/10"
    
    # 1. FILE_ID ORQALI (agar mavjud bo'lsa)
    if 'file_id' in film and film['file_id']:
        try:
            await update.message.chat.send_action("upload_video")
            
            await update.message.reply_video(
                video=film['file_id'],
                caption=caption
            )
            
            # Statistika
            db.increment_video(user_id)
            db.add_to_history(user_id, key)
            db.add_points(user_id, 3)
            return True
            
        except Exception as e:
            logger.warning(f"❌ File ID ishlamadi: {str(e)[:100]}")
    
    # 2. LOCAL FAYL
    video_path = film.get('video')
    if not video_path:
        await update.message.reply_text("❌ Bu film uchun video yo'q")
        return True
    
    if video_path.startswith('./') or video_path.startswith('videos/'):
        local_path = Path(video_path)
        
        if not local_path.exists():
            await update.message.reply_text(f"❌ Video fayl topilmadi: {video_path}")
            return True
        
        file_size = local_path.stat().st_size
        
        if file_size > 50 * 1024 * 1024:
            await update.message.reply_text(
                f"❌ Video juda katta ({file_size / 1024 / 1024:.1f}MB)\n\n"
                f"💡 Yechim:\n"
                f"1️⃣ Video'ni siqing (FFmpeg)\n"
                f"2️⃣ Telegram channel'ga yuklab, file_id ni saqlang\n"
                f"3️⃣ KATTA_FILMLAR_YECHIM.md ga qarang"
            )
            return True
        
        try:
            await update.message.chat.send_action("upload_video")
            
            with open(local_path, 'rb') as video_file:
                video_message = await update.message.reply_video(
                    video=video_file,
                    caption=caption
                )
                
                # FILE_ID ni saqlash (keyingi yuborishlar uchun)
                if video_message and video_message.video:
                    file_id = video_message.video.file_id
                    film['file_id'] = file_id
                    # JSON faylga saqlash
                    save_file_id_to_json(key, file_id)
                    logger.info(f"✅ File ID saqlandi: {key}")
            
            # Statistika
            db.increment_video(user_id)
            db.add_to_history(user_id, key)
            db.add_points(user_id, 3)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Video yuborishda xatolik: {str(e)[:100]}")
        
        return True
    
    return True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    text_lower = text.lower()
    user_id = update.effective_user.id

    # Admin qo'shish holati
    if context.user_data.get('pending_admin_add') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_admin_add']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        target_id = await _resolve_user_id_from_text(update, context, text)
        if not target_id:
            return
        if target_id in ADMIN_IDS:
            del context.user_data['pending_admin_add']
            await update.message.reply_text("ℹ️ Bu admin allaqachon config.py da mavjud")
            return
        if db.add_admin_id(target_id):
            refresh_admin_ids()
            del context.user_data['pending_admin_add']
            await update.message.reply_text(
                f"✅ Admin qo'shildi: <code>{target_id}</code>",
                parse_mode='HTML'
            )
            return
        await update.message.reply_text("ℹ️ Bu admin allaqachon ro'yxatda")
        return

    # Admin o'chirish holati
    if context.user_data.get('pending_admin_remove') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_admin_remove']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        target_id = await _resolve_user_id_from_text(update, context, text)
        if not target_id:
            return
        if target_id in ADMIN_IDS:
            del context.user_data['pending_admin_remove']
            await update.message.reply_text("❌ Bu admin config.py dan o'chiriladi")
            return
        if db.remove_admin_id(target_id):
            refresh_admin_ids()
            del context.user_data['pending_admin_remove']
            await update.message.reply_text(
                f"✅ Admin o'chirildi: <code>{target_id}</code>",
                parse_mode='HTML'
            )
            return
        await update.message.reply_text("ℹ️ Bu admin ro'yxatda yo'q")
        return

    # Post yuborish holati
    if context.user_data.get('pending_post') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_post']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        del context.user_data['pending_post']
        await _broadcast_message(update, context, text)
        return

    # Admin rolini o'rnatish holati
    if context.user_data.get('pending_setrole') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_setrole']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        parts = text.split()
        if len(parts) < 2:
            await update.message.reply_text("❌ Format noto'g'ri")
            return
        context.user_data.pop('pending_setrole', None)
        context.args = parts
        await setrole_command(update, context)
        return

    # Post kanalini sozlash holati
    if context.user_data.get('pending_setchannel') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_setchannel']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        context.user_data.pop('pending_setchannel', None)
        context.args = [text]
        await setchannel_command(update, context)
        return

    # Kanalga post yuborish holati
    if context.user_data.get('pending_postchannel') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_postchannel']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        context.user_data.pop('pending_postchannel', None)
        context.args = [text]
        await postchannel_command(update, context)
        return

    # Post rejalash holati
    if context.user_data.get('pending_schedulepost') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_schedulepost']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        context.user_data.pop('pending_schedulepost', None)
        context.args = [text]
        await schedulepost_command(update, context)
        return

    # Kanal post rejalash holati
    if context.user_data.get('pending_schedulepostchannel') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_schedulepostchannel']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        context.user_data.pop('pending_schedulepostchannel', None)
        context.args = [text]
        await schedulepostchannel_command(update, context)
        return

    # Film tahrir holati
    if context.user_data.get('pending_editfilm') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_editfilm']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        context.user_data.pop('pending_editfilm', None)
        context.args = [text]
        await editfilm_command(update, context)
        return

    # Film o'chirish holati
    if context.user_data.get('pending_deletefilm') and is_admin(user_id):
        if text_lower == '/cancel':
            del context.user_data['pending_deletefilm']
            await update.message.reply_text("❌ Bekor qilindi")
            return
        context.user_data.pop('pending_deletefilm', None)
        context.args = [text]
        await deletefilm_command(update, context)
        return
    
    # Film metadata qo'shish holati (admin uchun)
    if 'pending_file_id' in context.user_data and is_admin(user_id):
        # Agar bu metadata bo'lsa, handle qilamiz
        if '|' in text and not text.startswith('/'):
            # Format: title|year|rating|genre|director|description|key
            parts = [p.strip() for p in text.split('|')]
            
            if len(parts) != 7:
                await update.message.reply_text(
                    "❌ <b>Noto'g'ri format!</b>\n\n"
                    "Kerakli format:\n"
                    "<code>Title|Year|Rating|Genre|Director|Description|Key</code>\n\n"
                    "Misol:\n"
                    "<code>Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish haqida|inception</code>\n\n"
                    "7 ta qism kerak! (| bilan ajratilgan)",
                    parse_mode='HTML'
                )
                return
            
            try:
                title, year, rating, genre, director, description, key = parts
                
                # Validatsiya
                year = int(year)
                rating = float(rating)
                
                if not key.replace('_', '').replace('-', '').isalnum() or key != key.lower():
                    await update.message.reply_text(
                        "❌ Key noto'g'ri!\n\n"
                        "Key faqat kichik harflar, raqamlar va _ yoki - bo'lishi mumkin.\n"
                        "Misol: inception, dark_knight, matrix_2"
                    )
                    return
                
                # Film obyekti yaratish
                film = {
                    "key": key,
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "janr": genre,
                    "director": director,
                    "description": description,
                    "languages": ["python"],  # Default
                    "file_id": context.user_data['pending_file_id']
                }
                
                # JSON ga qo'shish
                json_file = "films_database.json"
                
                if os.path.exists(json_file):
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                else:
                    data = {"films": []}
                
                # Dublikat tekshirish
                duplicate_found = False
                for existing_film in data.get('films', []):
                    if existing_film.get('key') == key:
                        duplicate_found = True
                        break
                
                if duplicate_found:
                    await update.message.reply_text(
                        f"⚠️ <b>Film allaqachon mavjud!</b>\n\n"
                        f"Key: <code>{key}</code>\n\n"
                        "Boshqa key tanlang yoki mavjud filmni o'chiring.",
                        parse_mode='HTML'
                    )
                    return
                
                # Film qo'shish
                data['films'].append(film)
                
                # Faylga yozish
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                await update.message.reply_text(
                    f"✅ <b>Film muvaffaqiyatli qo'shildi!</b>\n\n"
                    f"🎬 <b>{title}</b> ({year})\n"
                    f"⭐ {rating}/10\n"
                    f"🎭 {genre}\n"
                    f"👤 {director}\n"
                    f"📝 {description[:60]}...\n"
                    f"🔑 Key: <code>{key}</code>\n\n"
                    f"💾 <code>{json_file}</code> ga saqlandi!\n\n"
                    f"🔄 <b>Bot'ni restart qiling:</b>\n"
                    f"Ctrl+C bosing va qayta <code>python filimuz.py</code> ishga tushiring\n\n"
                    f"📊 Jami filmlar: {len(data['films'])}",
                    parse_mode='HTML'
                )
                
                logger.info(f"✅ Yangi film qo'shildi: {key} - {title}")
                log_admin_action(user_id, "ADD_FILM", key)

                # In-memory movies yangilash
                film_copy = film.copy()
                film_copy.pop('key', None)
                movies[key] = film_copy
                
                # Pending file_id ni tozalash
                del context.user_data['pending_file_id']
                return
                
            except ValueError:
                await update.message.reply_text(
                    f"❌ <b>Ma'lumot xato!</b>\n\n"
                    f"Year va Rating raqam bo'lishi kerak.\n\n"
                    f"Misol:\n"
                    f"<code>Inception|2010|8.8|...</code>",
                    parse_mode='HTML'
                )
                return
            except Exception as e:
                await update.message.reply_text(f"❌ Xatolik: {str(e)}")
                logger.error(f"Film qo'shishda xato: {e}")
                return
    
    # Izoh qo'shish holati
    if 'pending_comment' in context.user_data:
        film_key = context.user_data['pending_comment']
        del context.user_data['pending_comment']
        
        if text_lower == '/cancel':
            await update.message.reply_text("❌ Bekor qilindi")
            return
        
        # Izohni saqlash
        username = update.effective_user.username
        db.add_comment(user_id, username, film_key, text)
        db.add_points(user_id, 15)  # 15 ball
        
        await update.message.reply_text("✅ Izohingiz saqlandi! +15 ball")
        
        # Filmni qayta ko'rsatish
        if film_key in movies:
            film = movies[film_key]
            message = format_film_info(film_key, film, user_id)
            keyboard = get_film_keyboard(user_id, film_key, show_video=True)
            await update.message.reply_text(message, parse_mode='HTML', reply_markup=keyboard)
        
        return
    
    # Avval raqam tekshirish
    if text.isdigit():
        handled = await handle_number(update, context)
        if handled:
            return
    
    # URL detektsiya (YouTube, Instagram) - ASLIY textdan URL ol!
    if "youtube.com" in text_lower or "youtu.be" in text_lower or "instagram.com" in text_lower:
        try:
            # URL topildi - video download sifatida ishlay
            # Telegram message -> /ig command ga aylantir
            from unittest.mock import MagicMock
            
            # Fake context.args yaratamiz
            new_context = type('obj', (object,), {'args': [text]})()
            await download_instagram(update, new_context)
            return
        except Exception as e:
            await update.message.reply_text(f"[ERROR] URL muammosi: {str(e)[:80]}")
            return
    
    # Oddiy film qidirish - text_lower ishlat
    # Aniq qidiruv
    if text_lower in movies:
        film = movies[text_lower]
        message = f"[FILM] <b>{film['title']}</b>\n"
        message += f"[YIL] {film['year']}\n"
        message += f"[REYTING] {film['rating']}/10\n"
        message += f"[JANR] {film['janr']}\n"
        message += f"[DIRECTOR] {film['director']}\n"
        message += f"[DESC] {film['description']}"
        await update.message.reply_text(message, parse_mode='HTML')
        return
    
    # Fuzzy qidiruv - nomda, directorga yoki janrga qayta qidirish
    matches = []
    for key, film in movies.items():
        title_match = text_lower in film['title'].lower()
        director_match = text_lower in film['director'].lower()
        key_match = text_lower in key
        
        if title_match or director_match or key_match:
            matches.append((key, film))
     
    if matches:
        if len(matches) == 1:
            # Bitta topilsa uni ko'rsatish
            key, film = matches[0]
            message = f"[FILM] <b>{film['title']}</b>\n"
            message += f"[YIL] {film['year']}\n"
            message += f"[REYTING] {film['rating']}/10\n"
            message += f"[JANR] {film['janr']}\n"
            message += f"[DIRECTOR] {film['director']}\n"
            message += f"[DESC] {film['description']}"
            await update.message.reply_text(message, parse_mode='HTML')
        else:
            # Ko'plarsa ro'yxatini chiqarish
            message = "[RESULTS] Topilgan filmlar:\n\n"
            for i, (key, film) in enumerate(matches, 1):
                message += f"{i}. <b>{film['title']}</b> ({film['year']})\n"
                message += f"   Reyting: {film['rating']}/10\n\n"
            await update.message.reply_text(message, parse_mode='HTML')
    else:
        await update.message.reply_text(
            "[HELP] Film topilmadi!\n\n"
            "[QIDIRISH] inception, matrix, nolan...\n"
            "[VIDEO] YouTube yoki Instagram linki: https://...\n"
            "[AMALLAR] /start, /list, /top, /random, /kodli"
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugma bosish uchun handler"""
    text = update.message.text.strip()
    
    if text == "🎬 FILMLAR":
        await films_menu(update, context)
    elif text == "📥 VIDEO" or text == "📥 YOUTUBE/INSTAGRAM DOWNLOADER":
        await video_menu(update, context)

# ==================== YANGI FUNKSIYALAR ====================

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi profili"""
    user_id = update.effective_user.id
    user_data = db.get_all_users().get(str(user_id), {})
    
    if not user_data:
        await update.message.reply_text("❌ Profil topilmadi")
        return
    
    premium_status = "💎 Premium" if db.is_premium(user_id) else "🆓 Oddiy"
    lang_name = {"uz": "🇺🇿 O'zbek", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"}
    user_lang = db.get_language(user_id)
    
    message = f"👤 <b>PROFIL</b>\n\n"
    message += f"👨‍💻 {user_data.get('first_name', 'Foydalanuvchi')}\n"
    if user_data.get('username'):
        message += f"📱 @{user_data['username']}\n"
    message += f"\n{premium_status}\n\n"
    message += f"📅 Qo'shilgan: {user_data['joined_at'][:10]}\n"
    message += f"⚡ Buyruqlar: {user_data.get('commands_used', 0)}\n"
    message += f"🎬 Videolar: {user_data.get('videos_watched', 0)}\n"
    message += f"⭐ Sevimlilar: {len(db.get_favorites(user_id))}\n"
    message += f"💰 Ballar: {db.get_points(user_id)}\n"
    message += f"🌐 Til: {lang_name.get(user_lang, user_lang)}"
    
    # Inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("⭐ Sevimlilar", callback_data="show_favorites"),
            InlineKeyboardButton("📜 Tarix", callback_data="show_history")
        ],
        [
            InlineKeyboardButton("⚙️ Sozlamalar", callback_data="show_settings")
        ]
    ]
    
    if not db.is_premium(user_id):
        keyboard.append([InlineKeyboardButton("💎 Premium olish", callback_data="get_premium")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)

async def favorites_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sevimlilar ro'yxati"""
    user_id = update.effective_user.id
    favorites = db.get_favorites(user_id)
    
    if not favorites:
        await update.message.reply_text("⭐ Sevimlilar ro'yxati bo'sh\n\nFilmlarni ko'rib, ⭐ tugmasini bosing!")
        return
    
    message = "⭐ <b>SEVIMLILAR RO'YXATI</b>\n\n"
    
    for idx, film_key in enumerate(favorites, 1):
        if film_key in movies:
            film = movies[film_key]
            message += f"{idx}. <b>{film['title']}</b> ({film['year']})\n"
            message += f"   ⭐ {film['rating']}/10 | 🎭 {film['janr']}\n\n"
    
    await update.message.reply_text(message, parse_mode='HTML')

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ko'rilgan filmlar tarixi"""
    user_id = update.effective_user.id
    history = db.get_history(user_id, limit=20)
    
    if not history:
        await update.message.reply_text("📜 Ko'rilgan filmlar tarixi bo'sh\n\nFilmlarni tomosha qiling!")
        return
    
    message = "📜 <b>KO'RILGAN FILMLAR TARIXI</b>\n\n"
    
    for idx, entry in enumerate(history, 1):
        film_key = entry['film_key']
        date = entry['date'][:10]
        
        if film_key in movies:
            film = movies[film_key]
            message += f"{idx}. <b>{film['title']}</b>\n"
            message += f"   📅 {date} | ⭐ {film['rating']}/10\n\n"
    
    await update.message.reply_text(message, parse_mode='HTML')

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sozlamalar menu"""
    user_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton("🌐 Tilni o'zgartirish", callback_data="change_language")],
        [InlineKeyboardButton("🔔 Xabarnomalar", callback_data="notifications")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = "⚙️ <b>SOZLAMALAR</b>\n\nQaysi sozlamani o'zgartirmoqchisiz?"
    
    await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)

async def top_rated_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Eng yuqori baholangan filmlar"""
    top_films = db.get_top_rated_films(limit=10)
    
    if not top_films:
        await update.message.reply_text("📊 Hozircha baholangan filmlar yo'q")
        return
    
    message = "🏆 <b>ENG YUQORI BAHOLANGAN FILMLAR</b>\n\n"
    
    for idx, (film_key, avg_rating, count) in enumerate(top_films, 1):
        if film_key in movies:
            film = movies[film_key]
            message += f"{idx}. <b>{film['title']}</b>\n"
            message += f"   ⭐ {avg_rating}/10 ({count} ta baho)\n\n"
    
    await update.message.reply_text(message, parse_mode='HTML')

async def most_watched_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Eng ko'p ko'rilgan filmlar"""
    most_watched = db.get_most_watched_films(limit=10)
    
    if not most_watched:
        await update.message.reply_text("📊 Hozircha statistika yo'q")
        return
    
    message = "🔥 <b>ENG KO'P KO'RILGAN FILMLAR</b>\n\n"
    
    for idx, (film_key, count) in enumerate(most_watched, 1):
        if film_key in movies:
            film = movies[film_key]
            message += f"{idx}. <b>{film['title']}</b>\n"
            message += f"   👁️ {count} marta ko'rilgan\n\n"
    
    await update.message.reply_text(message, parse_mode='HTML')

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Top foydalanuvchilar"""
    top_users = db.get_top_users(limit=10)
    
    if not top_users:
        await update.message.reply_text("📊 Hozircha statistika yo'q")
        return
    
    message = "🏆 <b>TOP FOYDALANUVCHILAR</b>\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    
    for idx, (uid, username, first_name, points, videos) in enumerate(top_users, 1):
        medal = medals[idx-1] if idx <= 3 else f"{idx}."
        name = f"@{username}" if username else first_name
        message += f"{medal} {name}\n"
        message += f"   💰 {points} ball | 🎬 {videos} video\n\n"
    
    await update.message.reply_text(message, parse_mode='HTML')

# ==================== CALLBACK QUERY HANDLER ====================

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline keyboard callback handler"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    # WATCH VIDEO
    if data.startswith("watch_"):
        film_key = data.replace("watch_", "")
        if film_key in movies:
            # Raqamni topish
            film_list = list(movies.keys())
            film_number = film_list.index(film_key) + 1
            
            # handle_number funksiyasiga o'tkazish
            context.user_data['pending_video'] = film_key
            await query.edit_message_text(f"⏳ Video yuklanmoqda...\n\n{movies[film_key]['title']}")
            
            # Video yuborish
            await send_video_by_key(query, context, user_id, film_key)
    
    # FAVORITE/UNFAVORITE
    elif data.startswith("fav_"):
        film_key = data.replace("fav_", "")
        db.add_favorite(user_id, film_key)
        db.add_points(user_id, 5)  # 5 ball
        
        if film_key in movies:
            film = movies[film_key]
            new_keyboard = get_film_keyboard(user_id, film_key, show_video=True)
            await query.edit_message_reply_markup(reply_markup=new_keyboard)
            await query.answer("✅ Sevimlilar ro'yxatiga qo'shildi! +5 ball", show_alert=True)
    
    elif data.startswith("unfav_"):
        film_key = data.replace("unfav_", "")
        db.remove_favorite(user_id, film_key)
        
        if film_key in movies:
            film = movies[film_key]
            new_keyboard = get_film_keyboard(user_id, film_key, show_video=True)
            await query.edit_message_reply_markup(reply_markup=new_keyboard)
            await query.answer("✅ Sevimlilardan o'chirildi", show_alert=True)
    
    # RATING
    elif data.startswith("rate_"):
        film_key = data.replace("rate_", "")
        
        # Rating keyboard
        keyboard = []
        row = []
        for i in range(1, 11):
            row.append(InlineKeyboardButton(f"⭐{i}", callback_data=f"rating_{film_key}_{i}"))
            if i % 5 == 0:
                keyboard.append(row)
                row = []
        
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data=f"back_{film_key}")])
        
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
        await query.answer("⭐ 1-10 oralig'ida baho bering")
    
    elif data.startswith("rating_"):
        parts = data.split("_")
        film_key = parts[1]
        rating = int(parts[2])
        
        db.add_rating(user_id, film_key, rating)
        db.add_points(user_id, 10)  # 10 ball
        
        if film_key in movies:
            film = movies[film_key]
            new_keyboard = get_film_keyboard(user_id, film_key, show_video=True)
            await query.edit_message_reply_markup(reply_markup=new_keyboard)
            await query.answer(f"✅ {rating}⭐ baho qo'yildi! +10 ball", show_alert=True)
    
    # COMMENTS
    elif data.startswith("comments_"):
        film_key = data.replace("comments_", "")
        comments = db.get_comments(film_key, limit=5)
        
        if not comments:
            message = f"💬 <b>{movies[film_key]['title']}</b>\n\n❌ Hozircha izohlar yo'q\n\nBirinchi bo'lib izoh qoldiring!"
        else:
            message = f"💬 <b>{movies[film_key]['title']}</b>\n\n"
            for comment in comments:
                username = comment['username'] or "Anonim"
                message += f"👤 @{username}\n📝 {comment['text']}\n📅 {comment['date'][:10]}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("➕ Izoh qo'shish", callback_data=f"add_comment_{film_key}")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data=f"back_{film_key}")]
        ]
        
        await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith("add_comment_"):
        film_key = data.replace("add_comment_", "")
        context.user_data['pending_comment'] = film_key
        await query.edit_message_text(
            "💬 Izohingizni yuboring:\n\n(Bekor qilish uchun /cancel)",
            parse_mode='HTML'
        )
    
    # BACK
    elif data.startswith("back_"):
        film_key = data.replace("back_", "")
        if film_key in movies:
            film = movies[film_key]
            message = format_film_info(film_key, film, user_id)
            keyboard = get_film_keyboard(user_id, film_key, show_video=True)
            await query.edit_message_text(message, parse_mode='HTML', reply_markup=keyboard)
    
    # PROFILE ACTIONS
    elif data == "show_favorites":
        await query.message.delete()
        await favorites_command(query, context)
    
    elif data == "show_history":
        await query.message.delete()
        await history_command(query, context)
    
    elif data == "show_settings":
        await query.message.delete()
        await settings_command(query, context)
    
    # LANGUAGE CHANGE
    elif data == "change_language":
        keyboard = [
            [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz")],
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back_settings")]
        ]
        
        await query.edit_message_text(
            "🌐 <b>TILNI TANLANG</b>\n\nSelect your language:",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data.startswith("lang_"):
        lang = data.replace("lang_", "")
        db.set_language(user_id, lang)
        
        lang_names = {"uz": "O'zbek", "ru": "Русский", "en": "English"}
        await query.answer(f"✅ Til o'zgartirildi: {lang_names[lang]}", show_alert=True)
        await query.message.delete()
        
        # Yangi tilga o'tish
        await settings_command(query, context)
    
    # PREMIUM
    elif data == "get_premium":
        message = (
            "💎 <b>PREMIUM</b>\n\n"
            "<b>Xususiyatlar:</b>\n"
            "✅ HD video yuklovchi\n"
            "✅ Cheksiz sevimlilar\n"
            "✅ Reklama yo'q\n"
            "✅ Yangi filmlar birinchi bo'lib\n"
            "✅ Shaxsiy tavsiyalar\n\n"
            "💰 Narx: 50,000 so'm/oy\n\n"
            "📞 Admin: @your_admin"
        )
        
        keyboard = [[InlineKeyboardButton("📞 Admin bilan bog'lanish", url="https://t.me/your_admin")]]
        
        await query.edit_message_text(message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

async def send_video_by_key(query, context, user_id, film_key):
    """Film keyiga ko'ra video yuborish (file_id yoki local fayl)"""
    if film_key not in movies:
        return
    
    film = movies[film_key]
    caption = f"🎬 {film['title']} ({film['year']}) | ⭐ {film['rating']}/10"
    
    # 1. FILE_ID ORQALI (Telegram cloud'dan, 50MB limitidan farqli, 2GB gacha)
    if 'file_id' in film and film['file_id']:
        try:
            await query.message.reply_video(
                video=film['file_id'],
                caption=caption
            )
            
            # Statistika
            db.increment_video(user_id)
            db.add_to_history(user_id, film_key)
            db.add_points(user_id, 3)
            return
            
        except Exception as e:
            # Agar file_id ishlamasa, local faylga o'tamiz
            logger.warning(f"❌ File ID ishlamadi: {str(e)[:100]}")
    
    # 2. LOCAL FAYL
    video_path = film.get('video')
    
    if not video_path:
        await query.message.reply_text("❌ Bu film uchun video yo'q")
        return
    
    if video_path.startswith('./') or video_path.startswith('videos/'):
        local_path = Path(video_path)
        
        if not local_path.exists():
            await query.message.reply_text(f"❌ Video fayl topilmadi: {video_path}")
            return
        
        file_size = local_path.stat().st_size
        
        if file_size > 50 * 1024 * 1024:
            await query.message.reply_text(
                f"❌ Video juda katta ({file_size / 1024 / 1024:.1f}MB)\n\n"
                f"💡 Yechim:\n"
                f"1️⃣ Video'ni siqing (FFmpeg)\n"
                f"2️⃣ Telegram channel'ga yuklab, file_id ni saqlang\n"
                f"3️⃣ KATTA_FILMLAR_YECHIM.md ga qarang"
            )
            return
        
        try:
            with open(local_path, 'rb') as video_file:
                video_message = await query.message.reply_video(
                    video=video_file,
                    caption=caption
                )
                
                # FILE_ID ni saqlash (keyingi yuborishlar uchun)
                if video_message and video_message.video:
                    file_id = video_message.video.file_id
                    film['file_id'] = file_id
                    # JSON faylga saqlash
                    save_file_id_to_json(film_key, file_id)
                    logger.info(f"✅ File ID saqlandi: {film_key}")
            
            # Statistika
            db.increment_video(user_id)
            db.add_to_history(user_id, film_key)
            db.add_points(user_id, 3)  # 3 ball
            
        except Exception as e:
            await query.message.reply_text(f"❌ Video yuborishda xatolik: {str(e)[:100]}")


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN .env faylda topilmadi!")
    
    import time
    
    # Telegram API da muammolar bo'lsa qayta urinish
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            app = ApplicationBuilder().token(token).build()

            # Rejalashtirilgan postlarni qayta yuklash
            schedule_pending_posts(app)

            # Asosiy komandalar
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("list", list_movies))
            app.add_handler(CommandHandler("top", top_movies))
            app.add_handler(CommandHandler("random", random_movie))
            app.add_handler(CommandHandler("kodli", code_movies))
            
            # Dasturlash tillari
            app.add_handler(CommandHandler("python", python_movies))
            app.add_handler(CommandHandler("cpp", cpp_movies))
            app.add_handler(CommandHandler("csharp", csharp_movies))
            app.add_handler(CommandHandler("php", php_movies))
            app.add_handler(CommandHandler("java", java_movies))
            
            # Video yuklovchi
            app.add_handler(CommandHandler("ig", download_instagram))
            app.add_handler(CommandHandler("help", help_command))
            
            # Yangi foydalanuvchi komandalar
            app.add_handler(CommandHandler("profile", profile_command))
            app.add_handler(CommandHandler("favorites", favorites_command))
            app.add_handler(CommandHandler("history", history_command))
            app.add_handler(CommandHandler("settings", settings_command))
            app.add_handler(CommandHandler("toprated", top_rated_command))
            app.add_handler(CommandHandler("mostwatched", most_watched_command))
            app.add_handler(CommandHandler("leaderboard", leaderboard_command))
            
            # Admin komandalar
            app.add_handler(CommandHandler("admin", admin_panel))
            app.add_handler(CommandHandler("stats", stats_command))
            app.add_handler(CommandHandler("users", users_command))
            app.add_handler(CommandHandler("broadcast", broadcast_command))
            app.add_handler(CommandHandler("post", post_command))
            app.add_handler(CommandHandler("addpost", post_command))
            app.add_handler(CommandHandler("postchannel", postchannel_command))
            app.add_handler(CommandHandler("setchannel", setchannel_command))
            app.add_handler(CommandHandler("schedulepost", schedulepost_command))
            app.add_handler(CommandHandler("schedulepostchannel", schedulepostchannel_command))
            app.add_handler(CommandHandler("logs", logs_command))
            app.add_handler(CommandHandler("givepremium", give_premium_command))
            app.add_handler(CommandHandler("revokepremium", revoke_premium_command))
            app.add_handler(CommandHandler("cancel", cancel_command))
            app.add_handler(CommandHandler("addfilm", addfilm_command))
            app.add_handler(CommandHandler("editfilm", editfilm_command))
            app.add_handler(CommandHandler("deletefilm", deletefilm_command))
            app.add_handler(CommandHandler("importfilms", importfilms_command))
            app.add_handler(CommandHandler("addadmin", addadmin_command))
            app.add_handler(CommandHandler("removeadmin", removeadmin_command))
            app.add_handler(CommandHandler("listadmins", listadmins_command))
            app.add_handler(CommandHandler("setrole", setrole_command))
            
            # Callback query handler (inline buttons)
            app.add_handler(CallbackQueryHandler(callback_query_handler))

            # Import document handler
            app.add_handler(MessageHandler(filters.Document.ALL, handle_import_document))
            
            # Tugmalar uchun special handler (umum message handler dan oldin)
            app.add_handler(MessageHandler(
                filters.TEXT & ~filters.COMMAND & 
                (filters.Regex(r"^🎬 FILMLAR$") | filters.Regex(r"^📥")),
                button_handler
            ))
            
            # Oddiy xabar handler (film qidiruv, URL detektsiya, film metadata)
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

            print("[BOT] Bot ishga tushdi... (Ctrl+C bilan to'xtating)")
            print("[INFO] Soddalashtirilgan interfeys - faqat 2 ta tugma")
            print("  - 🎬 FILMLAR")
            print("  - 📥 VIDEO")
            app.run_polling()
            
        except KeyboardInterrupt:
            print("\n\n[BOT] Bot to'xtatildi.")
            break
        except Exception as e:
            if "Conflict" in str(e):
                
                retry_count += 1
                wait_time = 10 + (retry_count * 5)  # 15, 20, 25, 30, 35 seconds
                print(f"\n[WAIT] Telegram bilan bog'lanish muammosi ({retry_count}/{max_retries})")
                print(f"[WAIT] {wait_time} soniya kuting...")
                time.sleep(wait_time)
            else:
                print(f"[ERROR] Xato: {e}")
                raise

if __name__ == "__main__":
    main() 