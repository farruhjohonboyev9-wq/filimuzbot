#!/usr/bin/env python3
"""
ADMIN HANDLERS INTEGRATION - FILIMUZ BOT

Bu fayl admin panelni botga to'liq integratsiya qiladi
"""

from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler,
    ConversationHandler
)
from admin_panel_pro import (
    admin_panel,
    show_statistics,
    show_statistics_detail,
    show_users,
    show_films,
    show_premium,
    show_broadcast,
    show_system,
    show_analytics,
    show_database,
    back_to_admin
)

from admin_handlers import (
    admin_user_search,
    admin_top_users,
    admin_add_film,
    admin_film_list,
    admin_premium_give,
    admin_broadcast_text,
    admin_system_logs,
    admin_backup,
    admin_db_clean,
    admin_db_repair,
    admin_stats_export
)

def setup_admin_handlers(app: Application):
    """
    Admin handlerlari ro'yxatini o'rnatish
    
    Args:
        app: Telegram bot application
    """
    
    # MAIN ADMIN COMMAND
    app.add_handler(CommandHandler("admin", admin_panel))
    
    # CALLBACK HANDLERS
    callback_handlers = {
        # Admin Panel Navigation
        "admin_panel": back_to_admin,
        
        # Statistics
        "admin_stats": show_statistics,
        "admin_stats_detail": show_statistics_detail,
        
        # Users
        "admin_users": show_users,
        "admin_users_search": admin_user_search,
        "admin_users_top": admin_top_users,
        
        # Films
        "admin_films": show_films,
        "admin_films_add": admin_add_film,
        "admin_films_list": admin_film_list,
        
        # Premium
        "admin_premium": show_premium,
        "admin_premium_give": admin_premium_give,
        
        # Broadcast
        "admin_broadcast": show_broadcast,
        "admin_broadcast_text": admin_broadcast_text,
        
        # System
        "admin_system": show_system,
        "admin_system_logs": admin_system_logs,
        
        # Analytics
        "admin_analytics": show_analytics,
        
        # Database
        "admin_database": show_database,
        "admin_db_backup": admin_backup,
        "admin_db_clean": admin_db_clean,
        "admin_db_repair": admin_db_repair,
    }
    
    # Ro'yxatba qawqalt qilish
    for query_pattern, handler in callback_handlers.items():
        app.add_handler(CallbackQueryHandler(handler, pattern=f"^{query_pattern}$"))
    
    print("✅ Admin handlers ro'yxatga qo'shildi")

# Export for easy import
__all__ = ['setup_admin_handlers']
