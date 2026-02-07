#!/usr/bin/env python3
"""
TELEGRAM KANAL MONITOR

Telegram kanalga video yuklanganda avtomatik ravishda botga qo'shadi.
"""

import os
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token va admin ID
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

# Films database fayl
FILMS_DB = "films_database.json"

async def channel_video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanaldan video kelganda"""
    # Faqat channel postlari
    if not update.channel_post:
        return
    
    message = update.channel_post
    
    # Video bormi?
    if not message.video:
        return
    
    video = message.video
    file_id = video.file_id
    file_size = video.file_size / (1024 * 1024)  # MB
    duration = video.duration // 60  # Daqiqa
    
    # Caption dan film nomi olish
    caption = message.caption or "Yangi Film"
    
    logger.info(f"📹 Yangi video topildi: {caption}")
    logger.info(f"📦 Hajm: {file_size:.2f} MB | ⏰ {duration} min | File ID: {file_id}")
    
    # Adminga xabar yuborish
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=(
                    f"📹 <b>YANGI VIDEO KANALDA!</b>\n\n"
                    f"🎬 Nomi: {caption}\n"
                    f"📦 Hajm: {file_size:.2f} MB\n"
                    f"⏰ Davomiylik: {duration} daqiqa\n"
                    f"📐 O'lcham: {video.width}x{video.height}\n\n"
                    f"📹 File ID:\n<code>{file_id}</code>\n\n"
                    f"💡 Botga qo'shish uchun:\n"
                    f"/addfilm {file_id}"
                ),
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Adminga xabar yuborishda xato: {e}")

async def admin_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin komandalarini qayta ishlash"""
    user_id = update.effective_user.id
    
    # Admin tekshirish
    if user_id not in ADMIN_IDS:
        return
    
    text = update.message.text.strip()
    
    # /addfilm command
    if text.startswith('/addfilm'):
        parts = text.split(maxsplit=1)
        
        if len(parts) < 2:
            await update.message.reply_text(
                "❌ Xato format!\n\n"
                "Ishlatish:\n"
                "/addfilm FILE_ID"
            )
            return
        
        file_id = parts[1].strip()
        
        # Interaktiv qo'shish jarayoni
        await update.message.reply_text(
            "✅ Film qo'shish boshlandi!\n\n"
            "Quyidagi ma'lumotlarni yuboring:\n\n"
            "1️⃣ Film nomi (title)\n"
            "2️⃣ Yili (year)\n"
            "3️⃣ Reyting (rating)\n"
            "4️⃣ Janr (genre)\n"
            "5️⃣ Rezhissyor (director)\n"
            "6️⃣ Tavsif (description)\n"
            "7️⃣ Key (inglizcha, kichik harflar)\n\n"
            "Format:\n"
            "<code>Inception|2010|8.8|Sci-Fi|Christopher Nolan|Orzularga kirish|inception</code>",
            parse_mode='HTML'
        )
        
        # File ID ni saqlash (keyingi step uchun)
        context.user_data['pending_file_id'] = file_id

async def metadata_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Film metadata qabul qilish"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        return
    
    # Pending file_id bormi?
    if 'pending_file_id' not in context.user_data:
        return
    
    text = update.message.text.strip()
    
    # Format tekshirish: title|year|rating|genre|director|description|key
    parts = [p.strip() for p in text.split('|')]
    
    if len(parts) != 7:
        await update.message.reply_text(
            "❌ Noto'g'ri format!\n\n"
            "Kerakli format:\n"
            "<code>title|year|rating|genre|director|description|key</code>\n\n"
            "Misol:\n"
            "<code>Inception|2010|8.8|Sci-Fi, Thriller|Christopher Nolan|Orzularga kirish haqida|inception</code>",
            parse_mode='HTML'
        )
        return
    
    title, year, rating, genre, director, description, key = parts
    
    # Film obyekti yaratish
    film = {
        "key": key,
        "title": title,
        "year": int(year),
        "rating": float(rating),
        "janr": genre,
        "director": director,
        "description": description,
        "languages": ["python"],  # Default
        "file_id": context.user_data['pending_file_id']
    }
    
    # JSON ga qo'shish
    try:
        if os.path.exists(FILMS_DB):
            with open(FILMS_DB, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"films": []}
        
        # Film qo'shish
        data['films'].append(film)
        
        # Faylga yozish
        with open(FILMS_DB, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        await update.message.reply_text(
            f"✅ <b>Film muvaffaqiyatli qo'shildi!</b>\n\n"
            f"🎬 {title} ({year})\n"
            f"⭐ {rating}/10\n"
            f"🎭 {genre}\n"
            f"👤 {director}\n"
            f"🔑 Key: <code>{key}</code>\n\n"
            f"💾 {FILMS_DB} ga saqlandi!\n"
            f"🔄 Bot'ni restart qiling: <code>python filimuz.py</code>",
            parse_mode='HTML'
        )
        
        logger.info(f"✅ Yangi film qo'shildi: {key} - {title}")
        
        # Pending file_id ni tozalash
        del context.user_data['pending_file_id']
        
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")
        logger.error(f"Film qo'shishda xato: {e}")

def main():
    """Asosiy dastur"""
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN topilmadi!")
        return
    
    if not ADMIN_IDS:
        print("❌ ADMIN_IDS topilmadi!")
        return
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Kanal video handler
    app.add_handler(MessageHandler(filters.VIDEO & filters.ChatType.CHANNEL, channel_video_handler))
    
    # Admin komandalar
    app.add_handler(MessageHandler(filters.COMMAND & filters.ChatType.PRIVATE, admin_command_handler))
    
    # Metadata handler
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, metadata_handler))
    
    print("=" * 60)
    print("📺 TELEGRAM KANAL MONITOR")
    print("=" * 60)
    print()
    print("✅ Bot ishga tushdi!")
    print(f"👥 Adminlar: {ADMIN_IDS}")
    print()
    print("📝 Qanday ishlaydi:")
    print("1. Kanalga video yuklang")
    print("2. Bot avtomatik file_id ni oladi")
    print("3. Adminga xabar yuboradi")
    print("4. Admin /addfilm bilan qo'shadi")
    print()
    print("🔄 Monitor ishlamoqda...")
    print()
    
    # Bot ishga tushurish
    app.run_polling()

if __name__ == "__main__":
    main()
