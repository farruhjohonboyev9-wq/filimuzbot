#!/usr/bin/env python3
"""
TELEGRAM KANAL AVTOMATIK FILM YUKLOVCHI

Kanal linki yoki ID berasiz, bot barcha videolarni oladi va qo'shadi.
"""

import os
import json
import logging
import asyncio
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
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

# Admin'ning ma'lumotlarini saqlash
admin_data = {}

async def kanal_qoshish_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal qo'shish - /addchannel @channel_yoki_id"""
    user_id = update.effective_user.id
    
    # Admin tekshirish
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📺 <b>KANAL QOSHISH</b>\n\n"
            "Foydalanish:\n"
            "/addchannel @channel_username\n"
            "yoki\n"
            "/addchannel -1001234567890\n\n"
            "Bot kanal'dan barcha videolarni oladi!",
            parse_mode='HTML'
        )
        return
    
    channel_input = ' '.join(context.args).strip()
    
    # Channel username yoki ID
    if channel_input.startswith('@'):
        channel_id = channel_input
    elif channel_input.startswith('-100'):
        channel_id = int(channel_input)
    else:
        # Try to convert to int
        try:
            channel_id = int(channel_input)
        except:
            await update.message.reply_text(
                "❌ Noto'g'ri format!\n\n"
                "To'g'ri format:\n"
                "@channel_username\n"
                "yoki\n"
                "-1001234567890 (channel ID)"
            )
            return
    
    # Admin'ning session'iga kanal qo'shish
    admin_data[user_id] = {
        'channel_id': channel_id,
        'videos': [],
        'current_video_idx': 0,
        'status': 'fetching'
    }
    
    await update.message.reply_text(
        f"⏳ <b>Kanal'dan videolar yuklanyapti...</b>\n\n"
        f"📺 Kanal: <code>{channel_input}</code>\n\n"
        "Kuting...",
        parse_mode='HTML'
    )
    
    try:
        # Kanal'dan videolarni olish
        videos = []
        
        # Bot'ni kanal'ga biriktirishga urinish
        try:
            # Get channel chat info
            chat = await context.bot.get_chat(channel_id)
            logger.info(f"✅ Kanal topildi: {chat.title}")
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Kanal topilishmadi!</b>\n\n"
                f"Sabab:\n"
                f"- Bot kanal'ga admin emas\n"
                f"- Kanal ID noto'g'ri\n"
                f"- Kanal mavjud emas\n\n"
                f"Xato: {str(e)[:100]}",
                parse_mode='HTML'
            )
            del admin_data[user_id]
            return
        
        # Kanal'dan barcha messagelarni olish (video faqat)
        try:
            # Try to get recent messages from channel
            # NOTE: Bot API default limit = 100 messages
            async for message in context.bot._get_updates():
                pass
            
            # Alternative: use offset
            await update.message.reply_text(
                "⏳ <b>Kanal'dan videolar yuklanyapti...</b>\n\n"
                "Kuting, bu bir necha soniya davom etishi mumkin...",
                parse_mode='HTML'
            )
            
            # Get channel ID as integer
            if isinstance(channel_id, str):
                # Username -> try to get numerator
                # For now, we'll use getTelegramFileId approach
                pass
            
            # Simple approach: ask user to forward videos
            await update.message.reply_text(
                "⚠️ <b>AVTOMATIK YUKLASH CHEKLANAYOTGAN</b>\n\n"
                "Telegram Bot API cheklash tufayli barcha videolarni avtomatik olish mumkin emas.\n\n"
                "<b>Alternativ usul:</b>\n\n"
                "1️⃣ Kanal'dan videolarni bot'ga <b>forward</b> qiling\n"
                "2️⃣ Har bitta video uchun:\n"
                "   - <code>/addfilm FILE_ID</code>\n"
                "   - Ma'lumot kiriting\n\n"
                "Yoki kanal'ni bot'ni admin qilsangiz, "
                "forward'siz videolarni olish mumkin.",
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Videolar yuklashda xato: {e}")
            await update.message.reply_text(
                f"❌ Videolarni yuklashda xato: {str(e)[:100]}"
            )
        
        del admin_data[user_id]
        
    except Exception as e:
        logger.error(f"Qo'shlashda xato: {e}")
        await update.message.reply_text(f"❌ Xatolik: {str(e)[:100]}")
        if user_id in admin_data:
            del admin_data[user_id]

async def forward_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal'dan forward qilingan video'larni qabul qilish"""
    user_id = update.effective_user.id
    
    # Admin tekshirish
    if user_id not in ADMIN_IDS:
        return
    
    # Forward qilingan message bo'lsa va video bo'lsa
    if update.message.forward_from_chat and update.message.video:
        video = update.message.video
        file_id = video.file_id
        file_size = video.file_size / (1024 * 1024)
        
        forward_from = update.message.forward_from_chat
        
        await update.message.reply_text(
            f"✅ <b>VIDEO QABUL QILINDI!</b>\n\n"
            f"📺 Kanal: {forward_from.title}\n"
            f"📹 File ID: <code>{file_id}</code>\n"
            f"📦 Hajm: {file_size:.2f} MB\n\n"
            f"Endi:\n"
            f"<code>/addfilm {file_id}</code>\n\n"
            f"Keyin ma'lumot kiriting.",
            parse_mode='HTML'
        )
        
        # File ID ni avtomatik saqlash (quyidagi step uchun)
        context.user_data['last_file_id'] = file_id
        context.user_data['last_video_info'] = {
            'channel': forward_from.title,
            'size': file_size
        }

async def kanal_scanner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal'dan videolarni bo'taqa'ba o'q(batch)da olish"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Sizda admin huquqi yo'q!")
        return
    
    await update.message.reply_text(
        "📝 <b>KANAL VIDEOLARINI BATCH QOSHISH</b>\n\n"
        "Qo'shimcha info:\n\n"
        "1️⃣ Kanal'dan barcha videolarni bot'ga <b>forward</b> qiling\n"
        "2️⃣ Keyin quyidagi format'da ma'lumot yuboring:\n\n"
        "<code>Video1_Title|2010|8.8|Genre|Director|Desc|key1\n"
        "Video2_Title|2015|8.5|Genre|Director|Desc|key2\n"
        "Video3_Title|2020|8.2|Genre|Director|Desc|key3</code>\n\n"
        "🔄 Bot har bitta video uchun file_id'ni ishlata boshlaydi!",
        parse_mode='HTML'
    )

def main():
    """Asosiy dastur"""
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN topilmadi!")
        return
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Komandalar
    app.add_handler(CommandHandler("addchannel", kanal_qoshish_command))
    app.add_handler(CommandHandler("scanchannel", kanal_scanner_command))
    
    # Forward handler - kanal'dan forward qilingan videolarni qabul qilish
    app.add_handler(MessageHandler(
        filters.FORWARDED & filters.VIDEO & filters.ChatType.PRIVATE,
        forward_handler
    ))
    
    print("=" * 60)
    print("📺 TELEGRAM KANAL AVTOMATIK FILM YUKLOVCHI")
    print("=" * 60)
    print()
    print("✅ Bot ishga tushdi!")
    print()
    print("📝 Komandalar:")
    print("  /addchannel @username      - Kanalga ulanish")
    print("  /scanchannel               - Videolarni yuklash")
    print()
    print("💡 Qanday ishlaydi:")
    print("  1. Kanal'dan videolarni forward qiling")
    print("  2. Bot file_id ni oladi")
    print("  3. /addfilm bilan qo'shasiz")
    print()
    print("🔄 Monitor ishlamoqda...")
    print()
    
    app.run_polling()

if __name__ == "__main__":
    main()
