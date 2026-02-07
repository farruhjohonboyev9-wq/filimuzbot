#!/usr/bin/env python3
"""
FILE_ID OLISH VA SAQLASH UTILITY

Bu skript Telegram channel yoki botga yuklangan videolardan file_id ni avtomatik oladi.
"""

import os
from telegram import Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

# Bot token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

print("=" * 60)
print("📺 FILE_ID OLISH UTILITY")
print("=" * 60)
print()
print("🔧 Ishlatish:")
print("1. Bot'ga video jo'nating")
print("2. File ID avtomatik chiqadi")
print("3. Copy/paste qiling films_database.json ga")
print()
print("⚙️ Bot ishga tushmoqda...")
print()

async def video_handler(update, context):
    """Video yuborilganda file_id ni olish"""
    if update.message.video:
        video = update.message.video
        file_id = video.file_id
        file_size = video.file_size / (1024 * 1024)  # MB
        duration = video.duration // 60  # Daqiqa
        
        print("=" * 60)
        print("✅ VIDEO TOPILDI!")
        print("=" * 60)
        print(f"📹 File ID: {file_id}")
        print(f"📦 Hajm: {file_size:.2f} MB")
        print(f"⏰ Davomiylik: {duration} daqiqa")
        print(f"📐 O'lcham: {video.width}x{video.height}")
        print()
        print("📋 JSON uchun kod:")
        print("-" * 60)
        print(f'  "file_id": "{file_id}",')
        print("-" * 60)
        print()
        
        # Foydalanuvchiga javob
        await update.message.reply_text(
            f"✅ File ID olindi!\n\n"
            f"📹 File ID: `{file_id}`\n"
            f"📦 Hajm: {file_size:.2f} MB\n"
            f"⏰ Davomiylik: {duration} daqiqa\n\n"
            f"💾 films_database.json ga qo'shing!",
            parse_mode='Markdown'
        )

async def document_handler(update, context):
    """Document (video fayl) yuborilganda"""
    if update.message.document:
        doc = update.message.document
        
        # Video file mi?
        if doc.mime_type and doc.mime_type.startswith('video/'):
            file_id = doc.file_id
            file_size = doc.file_size / (1024 * 1024)  # MB
            
            print("=" * 60)
            print("✅ VIDEO DOCUMENT TOPILDI!")
            print("=" * 60)
            print(f"📹 File ID: {file_id}")
            print(f"📦 Hajm: {file_size:.2f} MB")
            print(f"📄 Fayl nomi: {doc.file_name}")
            print()
            print("📋 JSON uchun kod:")
            print("-" * 60)
            print(f'  "file_id": "{file_id}",')
            print("-" * 60)
            print()
            
            await update.message.reply_text(
                f"✅ File ID olindi!\n\n"
                f"📹 File ID: `{file_id}`\n"
                f"📦 Hajm: {file_size:.2f} MB\n"
                f"📄 Fayl: {doc.file_name}\n\n"
                f"💾 films_database.json ga qo'shing!",
                parse_mode='Markdown'
            )

def main():
    """Asosiy dastur"""
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN topilmadi!")
        print("💡 .env faylini yarating va tokenni qo'shing")
        return
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Video handler
    app.add_handler(MessageHandler(filters.VIDEO, video_handler))
    
    # Document handler
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))
    
    print("✅ Bot tayyor! Video jo'nating...")
    print()
    
    # Bot ishga tushurish
    app.run_polling()

if __name__ == "__main__":
    main()
