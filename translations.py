# -*- coding: utf-8 -*-
"""
Telegram Bot - Ko'p tillik tarjimalar
"""

TRANSLATIONS = {
    "uz": {
        # Asosiy
        "welcome": "🎬 <b>Salom! Film Botiga Xush Kelibsiz!</b>\n\n"
                   "Dasturlash tiliga qarab kinolar va video yuklovchi boti\n\n"
                   "💡 Raqam yuboring va video oling!\n"
                   "Masalan: /list buyrug'idan keyin raqam yuboring\n\n"
                   "Quyidagi tugmalardan birini bosing:",
        "films": "🎬 FILMLAR",
        "video": "📥 VIDEO",
        "profile": "👤 PROFIL",
        "favorites": "⭐ SEVIMLILAR",
        "history": "📜 TARIX",
        "settings": "⚙️ SOZLAMALAR",
        "back": "🔙 ORQAGA",
        
        # Film ma'lumotlari
        "watch_video": "▶️ Videoni ko'rish",
        "add_favorite": "⭐ Sevimlilar",
        "remove_favorite": "❌ Sevimlilardan",
        "rate_film": "⭐ Baholash",
        "add_comment": "💬 Izoh qoldirish",
        "view_comments": "💬 Izohlar",
        "share": "📤 Ulashish",
        
        # Profillar
        "your_profile": "👤 <b>SIZNING PROFILINGIZ</b>",
        "username": "Foydalanuvchi",
        "joined": "Qo'shilgan",
        "commands": "Buyruqlar",
        "videos_watched": "Ko'rilgan videolar",
        "favorites_count": "Sevimlilar",
        "points": "Ballar",
        "premium": "Premium",
        "language": "Til",
        
        # Sozlamalar
        "settings_menu": "⚙️ <b>SOZLAMALAR</b>\n\nQaysi sozlamani o'zgartirmoqchisiz?",
        "language_select": "Tilni tanlang:",
        "language_changed": "✅ Til o'zgartirildi!",
        
        # Sevimlilar
        "no_favorites": "❌ Sevimlilar ro'yxati bo'sh",
        "your_favorites": "⭐ <b>SIZNING SEVIMLILARINGIZ</b>",
        "added_to_favorites": "✅ Sevimlilar ro'yxatiga qo'shildi!",
        "removed_from_favorites": "✅ Sevimlilardan o'chirildi!",
        
        # Tarix
        "no_history": "❌ Ko'rilgan filmlar yo'q",
        "your_history": "📜 <b>KO'RILGAN FILMLAR TARIXI</b>",
        
        # Baholash
        "rate_prompt": "Filmni baholang (1-10):",
        "rating_saved": "✅ Sizning bahongiz saqlandi!",
        "your_rating": "Sizning bahongiz",
        "average_rating": "O'rtacha baho",
        "rating_count": "Baholar soni",
        
        # Izohlar
        "no_comments": "❌ Hozircha izohlar yo'q",
        "add_comment_prompt": "Izohingizni yuboring:",
        "comment_saved": "✅ Izohingiz saqlandi!",
        "comments_title": "💬 <b>IZOHLAR</b>",
        
        # Premium
        "premium_only": "💎 Bu xususiyat faqat Premium foydalanuvchilar uchun!",
        "get_premium": "💎 Premium olish",
        "premium_features": "💎 <b>PREMIUM XUSUSIYATLAR</b>\n\n"
                           "✅ HD video yuklovchi\n"
                           "✅ Cheksiz sevimlilar\n"
                           "✅ Reklama yo'q\n"
                           "✅ Yangi filmlar birinchi bo'lib\n"
                           "✅ Shaxsiy tavsiyalar",
        
        # Admin
        "admin_panel": "👤 <b>ADMIN PANEL</b>",
        "no_admin": "❌ Sizda admin huquqi yo'q!",
        
        # Xatolar
        "error": "❌ Xatolik yuz berdi",
        "not_found": "❌ Topilmadi",
        "invalid_input": "❌ Noto'g'ri ma'lumot",
    },
    
    "ru": {
        # Asosiy
        "welcome": "🎬 <b>Привет! Добро пожаловать в Фильм Бот!</b>\n\n"
                   "Бот для фильмов по языкам программирования и загрузчик видео\n\n"
                   "💡 Отправьте номер и получите видео!\n"
                   "Например: после команды /list отправьте номер\n\n"
                   "Выберите одну из кнопок ниже:",
        "films": "🎬 ФИЛЬМЫ",
        "video": "📥 ВИДЕО",
        "profile": "👤 ПРОФИЛЬ",
        "favorites": "⭐ ИЗБРАННОЕ",
        "history": "📜 ИСТОРИЯ",
        "settings": "⚙️ НАСТРОЙКИ",
        "back": "🔙 НАЗАД",
        
        # Информация о фильме
        "watch_video": "▶️ Смотреть видео",
        "add_favorite": "⭐ В избранное",
        "remove_favorite": "❌ Из избранного",
        "rate_film": "⭐ Оценить",
        "add_comment": "💬 Оставить комментарий",
        "view_comments": "💬 Комментарии",
        "share": "📤 Поделиться",
        
        # Профиль
        "your_profile": "👤 <b>ВАШ ПРОФИЛЬ</b>",
        "username": "Пользователь",
        "joined": "Присоединился",
        "commands": "Команды",
        "videos_watched": "Просмотрено видео",
        "favorites_count": "Избранное",
        "points": "Баллы",
        "premium": "Премиум",
        "language": "Язык",
        
        # Настройки
        "settings_menu": "⚙️ <b>НАСТРОЙКИ</b>\n\nКакую настройку вы хотите изменить?",
        "language_select": "Выберите язык:",
        "language_changed": "✅ Язык изменен!",
        
        # Избранное
        "no_favorites": "❌ Список избранного пуст",
        "your_favorites": "⭐ <b>ВАШЕ ИЗБРАННОЕ</b>",
        "added_to_favorites": "✅ Добавлено в избранное!",
        "removed_from_favorites": "✅ Удалено из избранного!",
        
        # История
        "no_history": "❌ Нет просмотренных фильмов",
        "your_history": "📜 <b>ИСТОРИЯ ПРОСМОТРА</b>",
        
        # Рейтинг
        "rate_prompt": "Оцените фильм (1-10):",
        "rating_saved": "✅ Ваша оценка сохранена!",
        "your_rating": "Ваша оценка",
        "average_rating": "Средний рейтинг",
        "rating_count": "Количество оценок",
        
        # Комментарии
        "no_comments": "❌ Пока нет комментариев",
        "add_comment_prompt": "Отправьте ваш комментарий:",
        "comment_saved": "✅ Комментарий сохранен!",
        "comments_title": "💬 <b>КОММЕНТАРИИ</b>",
        
        # Премиум
        "premium_only": "💎 Эта функция только для Premium пользователей!",
        "get_premium": "💎 Получить Premium",
        "premium_features": "💎 <b>ПРЕМИУМ ВОЗМОЖНОСТИ</b>\n\n"
                           "✅ HD загрузчик видео\n"
                           "✅ Неограниченное избранное\n"
                           "✅ Без рекламы\n"
                           "✅ Новые фильмы первыми\n"
                           "✅ Персональные рекомендации",
        
        # Админ
        "admin_panel": "👤 <b>ПАНЕЛЬ АДМИНА</b>",
        "no_admin": "❌ У вас нет прав администратора!",
        
        # Ошибки
        "error": "❌ Произошла ошибка",
        "not_found": "❌ Не найдено",
        "invalid_input": "❌ Неверные данные",
    },
    
    "en": {
        # Main
        "welcome": "🎬 <b>Hello! Welcome to Film Bot!</b>\n\n"
                   "Bot for movies by programming languages and video downloader\n\n"
                   "💡 Send a number and get the video!\n"
                   "For example: after /list command send a number\n\n"
                   "Choose one of the buttons below:",
        "films": "🎬 FILMS",
        "video": "📥 VIDEO",
        "profile": "👤 PROFILE",
        "favorites": "⭐ FAVORITES",
        "history": "📜 HISTORY",
        "settings": "⚙️ SETTINGS",
        "back": "🔙 BACK",
        
        # Film info
        "watch_video": "▶️ Watch Video",
        "add_favorite": "⭐ Add to Favorites",
        "remove_favorite": "❌ Remove from Favorites",
        "rate_film": "⭐ Rate",
        "add_comment": "💬 Add Comment",
        "view_comments": "💬 Comments",
        "share": "📤 Share",
        
        # Profile
        "your_profile": "👤 <b>YOUR PROFILE</b>",
        "username": "Username",
        "joined": "Joined",
        "commands": "Commands",
        "videos_watched": "Videos Watched",
        "favorites_count": "Favorites",
        "points": "Points",
        "premium": "Premium",
        "language": "Language",
        
        # Settings
        "settings_menu": "⚙️ <b>SETTINGS</b>\n\nWhich setting would you like to change?",
        "language_select": "Select language:",
        "language_changed": "✅ Language changed!",
        
        # Favorites
        "no_favorites": "❌ Favorites list is empty",
        "your_favorites": "⭐ <b>YOUR FAVORITES</b>",
        "added_to_favorites": "✅ Added to favorites!",
        "removed_from_favorites": "✅ Removed from favorites!",
        
        # History
        "no_history": "❌ No watched films",
        "your_history": "📜 <b>WATCH HISTORY</b>",
        
        # Rating
        "rate_prompt": "Rate the film (1-10):",
        "rating_saved": "✅ Your rating has been saved!",
        "your_rating": "Your rating",
        "average_rating": "Average rating",
        "rating_count": "Number of ratings",
        
        # Comments
        "no_comments": "❌ No comments yet",
        "add_comment_prompt": "Send your comment:",
        "comment_saved": "✅ Your comment has been saved!",
        "comments_title": "💬 <b>COMMENTS</b>",
        
        # Premium
        "premium_only": "💎 This feature is only for Premium users!",
        "get_premium": "💎 Get Premium",
        "premium_features": "💎 <b>PREMIUM FEATURES</b>\n\n"
                           "✅ HD video downloader\n"
                           "✅ Unlimited favorites\n"
                           "✅ No ads\n"
                           "✅ New films first\n"
                           "✅ Personal recommendations",
        
        # Admin
        "admin_panel": "👤 <b>ADMIN PANEL</b>",
        "no_admin": "❌ You don't have admin rights!",
        
        # Errors
        "error": "❌ An error occurred",
        "not_found": "❌ Not found",
        "invalid_input": "❌ Invalid input",
    }
}

def get_text(user_id, key, db):
    """Foydalanuvchi tili bo'yicha matnni olish"""
    lang = db.get_language(user_id)
    return TRANSLATIONS.get(lang, TRANSLATIONS["uz"]).get(key, key)

def format_text(user_id, key, db, **kwargs):
    """Formatlangan matnni olish"""
    text = get_text(user_id, key, db)
    return text.format(**kwargs) if kwargs else text
