#!/usr/bin/env python3
"""
KANAL LINKI ORQALI AVTOMATIK FILM QO'SHISH

Kanal linkini berasiz, bot videolarni oladi va qo'shadi.
"""

import os
import json
import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
FILMS_DB = "films_database.json"

# States
WAITING_CHANNEL = 1
WAITING_FOR_VIDEOS = 2
WAITING_FOR_METADATA = 3

# Session data
sessions = {}

async def kanal_link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal link qo'shish - /kanaldan @channel"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return WAITING_CHANNEL
    
    await update.message.reply_text(
        "📺 <b>KANAL ORQALI FILM QO'SHISH</b>\n\n"
        "<b>Kanal linkini yuboring:</b>\n\n"
        "Misol:\n"
        "•  t.me/mening_channel\n"
        "•  https://t.me/mening_channel\n"
        "•  @mening_channel\n"
        "•  -1001234567890 (Channel ID)\n\n"
        "Yoki /bekor qiling",
        parse_mode='HTML'
    )
    
    sessions[user_id] = {'step': 'waiting_link'}
    return WAITING_CHANNEL

async def process_channel_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal linkini qayta ishlash"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id not in ADMIN_IDS:
        return WAITING_CHANNEL
    
    if text == '/bekor':
        await update.message.reply_text("❌ Bekor qilindi.")
        if user_id in sessions:
            del sessions[user_id]
        return ConversationHandler.END
    
    # Kanal linkini parse qilsh
    channel_link = None
    channel_id = None
    
    # Format: @username
    if text.startswith('@'):
        channel_link = text
    
    # Format: https://t.me/username yoki t.me/username
    elif 't.me/' in text:
        match = re.search(r't\.me/([a-zA-Z0-9_]+)', text)
        if match:
            channel_link = '@' + match.group(1)
    
    # Format: -1001234567890 (ID)
    elif text.startswith('-100'):
        try:
            channel_id = int(text)
        except:
            pass
    
    if not channel_link and not channel_id:
        await update.message.reply_text(
            "❌ Noto'g'ri format!\n\n"
            "To'g'ri format:\n"
            "•  @mening_channel\n"
            "•  t.me/mening_channel\n"
            "•  -1001234567890"
        )
        return WAITING_CHANNEL
    
    # Kanal ma'lumotlarini saqlash
    sessions[user_id] = {
        'channel_link': channel_link or channel_id,
        'videos': [],
        'metadata': [],
        'step': 'waiting_videos'
    }
    
    await update.message.reply_text(
        f"✅ <b>KANAL QABUL QILINDI!</b>\n\n"
        f"📺 Kanal: <code>{channel_link or channel_id}</code>\n\n"
        f"<b>Endi:</b>\n"
        f"Kanal'dan videolarni bot'ga <b>forward</b> qiling.\n\n"
        f"Har bitta video'ni forward qiling (raqam bilan bo'lishi kerak).\n\n"
        f"Tayyoq bo'lganda: /tayyor\n"
        f"Bekor qilish: /bekor",
        parse_mode='HTML'
    )
    
    return WAITING_FOR_VIDEOS

async def receive_forwarded_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward qilingan videolarni qabul qilish"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS or user_id not in sessions:
        return WAITING_FOR_VIDEOS
    
    # Forward qilingan video?
    if update.message.forward_from_chat and update.message.video:
        video = update.message.video
        file_id = video.file_id
        file_size = video.file_size / (1024 * 1024)
        
        # Video'ni sessionga qo'shish
        video_info = {
            'file_id': file_id,
            'size': file_size,
            'width': video.width,
            'height': video.height,
            'duration': video.duration
        }
        
        sessions[user_id]['videos'].append(video_info)
        
        count = len(sessions[user_id]['videos'])
        
        await update.message.reply_text(
            f"✅ <b>VIDEO #{count} QABUL QILINDI</b>\n\n"
            f"📹 File ID: <code>{file_id[:50]}...</code>\n"
            f"📦 Hajm: {file_size:.2f} MB\n"
            f"📐 O'lcham: {video.width}x{video.height}\n"
            f"⏰ Davomiylik: {video.duration // 60} min\n\n"
            f"<b>Davom:</b>\n"
            f"• Yana video forward qiling\n"
            f"• /tayyor - ma'lumot kiritish\n"
            f"• /bekor - bekor qilish",
            parse_mode='HTML'
        )
        
        return WAITING_FOR_VIDEOS
    
    await update.message.reply_text(
        "⚠️ <b>FORWARD QILINGAN VIDEO KERAK!</b>\n\n"
        "Kanal'dan videolarni <b>forward</b> qiling.\n\n"
        "Yoki /tayyor bosing."
    )
    return WAITING_FOR_VIDEOS

async def ready_for_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Videolar jami, endi metadata"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS or user_id not in sessions:
        return WAITING_FOR_METADATA
    
    videos = sessions[user_id]['videos']
    
    if not videos:
        await update.message.reply_text(
            "❌ Video yo'q!\n"
            "Avval videolarni forward qiling."
        )
        return WAITING_FOR_VIDEOS
    
    await update.message.reply_text(
        f"✅ <b>TAYYOR!</b>\n\n"
        f"📊 Jami videolar: {len(videos)}\n\n"
        f"<b>Endi har bitta video uchun ma'lumot kiriting:</b>\n\n"
        f"Format:\n"
        f"<code>Title|Year|Rating|Genre|Director|Description|Key</code>\n\n"
        f"📋 Misol:\n"
        f"<code>Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish|inception</code>\n\n"
        f"<b>Tayyoqchi qaytaping!</b>\n\n"
        f"Video 1 uchun ma'lumot:",
        parse_mode='HTML'
    )
    
    sessions[user_id]['current_idx'] = 0
    return WAITING_FOR_METADATA

async def add_video_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Video uchun metadata qo'shish"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id not in ADMIN_IDS or user_id not in sessions:
        return WAITING_FOR_METADATA
    
    if text == '/bekor':
        if user_id in sessions:
            del sessions[user_id]
        await update.message.reply_text("❌ Bekor qilindi.")
        return ConversationHandler.END
    
    # Metadata parse qilish
    parts = [p.strip() for p in text.split('|')]
    
    if len(parts) != 7:
        await update.message.reply_text(
            "❌ <b>Noto'g'ri format!</b>\n\n"
            "Kerak: Title|Year|Rating|Genre|Director|Description|Key\n\n"
            "Qaytadan urinib ko'ring."
        )
        return WAITING_FOR_METADATA
    
    try:
        title, year, rating, genre, director, description, key = parts
        year = int(year)
        rating = float(rating)
        
        curr_idx = sessions[user_id]['current_idx']
        video = sessions[user_id]['videos'][curr_idx]
        
        # Film objekti
        film = {
            'key': key,
            'title': title,
            'year': year,
            'rating': rating,
            'janr': genre,
            'director': director,
            'description': description,
            'languages': ['python'],
            'file_id': video['file_id']
        }
        
        sessions[user_id]['metadata'].append(film)
        
        # Keyingi video bormi?
        curr_idx += 1
        
        if curr_idx < len(sessions[user_id]['videos']):
            sessions[user_id]['current_idx'] = curr_idx
            await update.message.reply_text(
                f"✅ <b>VIDEO #{curr_idx} QO'SHILDI</b>\n\n"
                f"🎬 {title} ({year})\n"
                f"⭐ {rating}/10\n\n"
                f"<b>Video #{curr_idx + 1} uchun ma'lumot:</b>"
            )
            return WAITING_FOR_METADATA
        
        # Barcha videolar qo'shildi
        return await save_all_films(update, context, user_id)
        
    except ValueError:
        await update.message.reply_text(
            "❌ <b>Ma'lumot xato!</b>\n\n"
            "Year va Rating raqam bo'lishi kerak.\n\n"
            "Qayta urinib ko'ring."
        )
        return WAITING_FOR_METADATA

async def save_all_films(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    """Barcha filmlarni JSON'ga saqlash"""
    metadata = sessions[user_id]['metadata']
    
    try:
        # JSON tugatish
        if os.path.exists(FILMS_DB):
            with open(FILMS_DB, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"films": []}
        
        # Barcha filmlarni qo'shish
        added = 0
        errors = []
        
        for film in metadata:
            # Dublikat tekshirish
            is_duplicate = False
            for existing in data['films']:
                if existing.get('key') == film['key']:
                    is_duplicate = True
                    errors.append(f"⚠️ {film['key']} allaqachon mavjud")
                    break
            
            if not is_duplicate:
                data['films'].append(film)
                added += 1
        
        # Saqlash
        with open(FILMS_DB, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Natija
        message = f"✅ <b>BARCHA FILMLAR QO'SHILDI!</b>\n\n"
        message += f"✅ Qo'shilgan: {added} ta\n"
        
        if errors:
            message += f"\n⚠️ Xatolar:\n"
            for error in errors[:5]:  # Birinchi 5 ta
                message += f"  {error}\n"
            if len(errors) > 5:
                message += f"  ... va yana {len(errors) - 5} ta"
        
        message += f"\n💾 <code>{FILMS_DB}</code> ga saqlandi!\n"
        message += f"📊 Jami filmlar: {len(data['films'])}\n\n"
        message += f"🔄 <b>Bot'ni restart qiling:</b>\n"
        message += f"<code>Ctrl+C</code> → <code>python filimuz.py</code>"
        
        await update.message.reply_text(message, parse_mode='HTML')
        
        logger.info(f"✅ {added} ta film qo'shildi")
        
        if user_id in sessions:
            del sessions[user_id]
        
        return ConversationHandler.END
        
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")
        logger.error(f"Saqlashda xato: {e}")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bekor qilish"""
    user_id = update.effective_user.id
    if user_id in sessions:
        del sessions[user_id]
    
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END

def main():
    """Asosiy dastur"""
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN topilmadi!")
        return
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('kanaldan', kanal_link_command)],
        states={
            WAITING_CHANNEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_channel_link)
            ],
            WAITING_FOR_VIDEOS: [
                MessageHandler(filters.FORWARDED & filters.VIDEO, receive_forwarded_video),
                CommandHandler('tayyor', ready_for_metadata)
            ],
            WAITING_FOR_METADATA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_video_metadata)
            ]
        },
        fallbacks=[CommandHandler('bekor', cancel)]
    )
    
    app.add_handler(conv_handler)
    
    print("=" * 60)
    print("📺 KANAL ORQALI AVTOMATIK FILM QO'SHISH")
    print("=" * 60)
    print()
    print("✅ Bot ishga tushdi!")
    print()
    print("📝 Komanda:")
    print("  /kanaldan        - Kanal link'i berib boshlang")
    print()
    print("📖 Jarayon:")
    print("  1. /kanaldan buyrug'i")
    print("  2. Kanal link'i yuboring")
    print("  3. Kanal'dan videolarni forward qiling")
    print("  4. /tayyor bosing")
    print("  5. Har bitta video uchun ma'lumot kiriting")
    print()
    print("🔄 Monitor ishlamoqda...")
    print()
    
    app.run_polling()

if __name__ == "__main__":
    main()
