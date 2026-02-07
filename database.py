import json
import os
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_file="database.json"):
        self.db_file = db_file
        self.data = self.load()
    
    def load(self):
        """Database yukla"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data.setdefault("admin_ids", [])
            data.setdefault("admin_roles", {})
            data.setdefault("settings", {})
            data.setdefault("scheduled_posts", [])
            data.setdefault("users", {})
            data.setdefault("favorites", {})
            data.setdefault("ratings", {})
            data.setdefault("comments", {})
            data.setdefault("watch_history", {})
            data.setdefault("premium_users", [])
            data.setdefault("user_languages", {})
            data.setdefault("stats", {
                "total_users": 0,
                "total_commands": 0,
                "total_videos_sent": 0,
                "bot_started": datetime.now().isoformat()
            })
            return data
        return {
            "admin_ids": [],
            "admin_roles": {},
            "settings": {},
            "scheduled_posts": [],
            "users": {},
            "favorites": {},  # user_id: [film_keys]
            "ratings": {},    # film_key: {user_id: rating}
            "comments": {},   # film_key: [{user_id, username, text, date}]
            "watch_history": {},  # user_id: [{film_key, date}]
            "premium_users": [],  # [user_ids]
            "user_languages": {},  # user_id: "uz"/"ru"/"en"
            "stats": {
                "total_users": 0,
                "total_commands": 0,
                "total_videos_sent": 0,
                "bot_started": datetime.now().isoformat()
            }
        }
    
    def save(self):
        """Database saqlash"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def add_user(self, user_id, username, first_name):
        """Yangi foydalanuvchi qo'shish"""
        if str(user_id) not in self.data["users"]:
            self.data["users"][str(user_id)] = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "joined_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat(),
                "commands_used": 0,
                "videos_watched": 0,
                "is_premium": False,
                "points": 0
            }
            self.data["stats"]["total_users"] += 1
            
            # Initialize user data
            if str(user_id) not in self.data.get("favorites", {}):
                self.data.setdefault("favorites", {})[str(user_id)] = []
            if str(user_id) not in self.data.get("watch_history", {}):
                self.data.setdefault("watch_history", {})[str(user_id)] = []
            if str(user_id) not in self.data.get("user_languages", {}):
                self.data.setdefault("user_languages", {})[str(user_id)] = "uz"
            
            self.save()
            return True
        else:
            # Foydalanuvchi mavjud - faqat last_active yangilash
            self.data["users"][str(user_id)]["last_active"] = datetime.now().isoformat()
            self.save()
            return False
    
    def increment_command(self, user_id):
        """Komanda hisobini oshirish"""
        if str(user_id) in self.data["users"]:
            self.data["users"][str(user_id)]["commands_used"] += 1
            self.data["stats"]["total_commands"] += 1
            self.save()
    
    def increment_video(self, user_id):
        """Video hisobini oshirish"""
        if str(user_id) in self.data["users"]:
            self.data["users"][str(user_id)]["videos_watched"] += 1
            self.data["stats"]["total_videos_sent"] += 1
            self.save()
    
    def get_stats(self):
        """Statistikani olish"""
        return self.data["stats"]
    
    def get_all_users(self):
        """Barcha foydalanuvchilarni olish"""
        return self.data["users"]
    
    def get_user_ids(self):
        """Barcha user ID larni olish"""
        return [int(uid) for uid in self.data["users"].keys()]

    # ADMINS
    def get_admin_ids(self):
        """Admin ID larni olish"""
        return [int(x) for x in self.data.get("admin_ids", [])]

    def add_admin_id(self, user_id):
        """Admin ID qo'shish"""
        admin_ids = self.data.setdefault("admin_ids", [])
        if user_id not in admin_ids:
            admin_ids.append(user_id)
            self.save()
            return True
        return False

    def remove_admin_id(self, user_id):
        """Admin ID o'chirish"""
        admin_ids = self.data.setdefault("admin_ids", [])
        if user_id in admin_ids:
            admin_ids.remove(user_id)
            self.save()
            return True
        return False

    def set_admin_role(self, user_id, role):
        """Admin rolini o'rnatish"""
        roles = self.data.setdefault("admin_roles", {})
        roles[str(user_id)] = role
        self.save()

    def get_admin_role(self, user_id):
        """Admin rolini olish"""
        return self.data.get("admin_roles", {}).get(str(user_id))

    # SETTINGS
    def set_setting(self, key, value):
        """Sozlamani saqlash"""
        self.data.setdefault("settings", {})[key] = value
        self.save()

    def get_setting(self, key, default=None):
        """Sozlamani olish"""
        return self.data.get("settings", {}).get(key, default)

    # SCHEDULED POSTS
    def add_scheduled_post(self, post):
        """Rejalashtirilgan post qo'shish"""
        self.data.setdefault("scheduled_posts", []).append(post)
        self.save()

    def remove_scheduled_post(self, post_id):
        """Rejalashtirilgan post o'chirish"""
        posts = self.data.setdefault("scheduled_posts", [])
        before = len(posts)
        posts = [p for p in posts if p.get("id") != post_id]
        self.data["scheduled_posts"] = posts
        self.save()
        return len(posts) != before

    def get_scheduled_posts(self):
        """Rejalashtirilgan postlar"""
        return list(self.data.get("scheduled_posts", []))
    
    # ==================== YANGI FUNKSIYALAR ====================
    
    # FAVORITES
    def add_favorite(self, user_id, film_key):
        """Sevimlilar ro'yxatiga qo'shish"""
        uid = str(user_id)
        if uid not in self.data.setdefault("favorites", {}):
            self.data["favorites"][uid] = []
        if film_key not in self.data["favorites"][uid]:
            self.data["favorites"][uid].append(film_key)
            self.save()
            return True
        return False
    
    def remove_favorite(self, user_id, film_key):
        """Sevimlilardan o'chirish"""
        uid = str(user_id)
        if uid in self.data.get("favorites", {}) and film_key in self.data["favorites"][uid]:
            self.data["favorites"][uid].remove(film_key)
            self.save()
            return True
        return False
    
    def get_favorites(self, user_id):
        """Foydalanuvchi sevimlilarini olish"""
        return self.data.get("favorites", {}).get(str(user_id), [])
    
    def is_favorite(self, user_id, film_key):
        """Film sevimlilar ro'yxatidami?"""
        return film_key in self.get_favorites(user_id)
    
    # WATCH HISTORY
    def add_to_history(self, user_id, film_key):
        """Ko'rilgan filmlar tarixiga qo'shish"""
        uid = str(user_id)
        if uid not in self.data.setdefault("watch_history", {}):
            self.data["watch_history"][uid] = []
        
        # Oxirgi 100 ta saqlash
        history_entry = {
            "film_key": film_key,
            "date": datetime.now().isoformat()
        }
        self.data["watch_history"][uid].insert(0, history_entry)
        self.data["watch_history"][uid] = self.data["watch_history"][uid][:100]
        self.save()
    
    def get_history(self, user_id, limit=10):
        """Foydalanuvchi tarixini olish"""
        return self.data.get("watch_history", {}).get(str(user_id), [])[:limit]
    
    # RATINGS
    def add_rating(self, user_id, film_key, rating):
        """Film uchun baho qo'yish (1-10)"""
        if film_key not in self.data.setdefault("ratings", {}):
            self.data["ratings"][film_key] = {}
        self.data["ratings"][film_key][str(user_id)] = {
            "rating": rating,
            "date": datetime.now().isoformat()
        }
        self.save()
    
    def get_user_rating(self, user_id, film_key):
        """Foydalanuvchi bahosini olish"""
        ratings = self.data.get("ratings", {}).get(film_key, {})
        user_rating = ratings.get(str(user_id))
        return user_rating["rating"] if user_rating else None
    
    def get_average_rating(self, film_key):
        """Film o'rtacha bahosini hisoblash"""
        ratings = self.data.get("ratings", {}).get(film_key, {})
        if not ratings:
            return None
        total = sum(r["rating"] for r in ratings.values())
        return round(total / len(ratings), 1)
    
    def get_rating_count(self, film_key):
        """Film nechta baho olgan"""
        return len(self.data.get("ratings", {}).get(film_key, {}))
    
    # COMMENTS
    def add_comment(self, user_id, username, film_key, text):
        """Film uchun izoh qo'shish"""
        if film_key not in self.data.setdefault("comments", {}):
            self.data["comments"][film_key] = []
        
        comment = {
            "user_id": user_id,
            "username": username,
            "text": text,
            "date": datetime.now().isoformat()
        }
        self.data["comments"][film_key].append(comment)
        self.save()
    
    def get_comments(self, film_key, limit=10):
        """Film izohlarini olish"""
        comments = self.data.get("comments", {}).get(film_key, [])
        return comments[-limit:][::-1]  # Oxirgi izohlar
    
    def get_comment_count(self, film_key):
        """Film nechta izoh olgan"""
        return len(self.data.get("comments", {}).get(film_key, []))
    
    # PREMIUM
    def set_premium(self, user_id, is_premium=True):
        """Premium statusni o'zgartirish"""
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["is_premium"] = is_premium
            
            premium_list = self.data.setdefault("premium_users", [])
            if is_premium and user_id not in premium_list:
                premium_list.append(user_id)
            elif not is_premium and user_id in premium_list:
                premium_list.remove(user_id)
            
            self.save()
    
    def is_premium(self, user_id):
        """Foydalanuvchi premium a'zomi?"""
        uid = str(user_id)
        return self.data.get("users", {}).get(uid, {}).get("is_premium", False)
    
    # POINTS
    def add_points(self, user_id, points):
        """Ball qo'shish"""
        uid = str(user_id)
        if uid in self.data["users"]:
            self.data["users"][uid]["points"] = self.data["users"][uid].get("points", 0) + points
            self.save()
    
    def get_points(self, user_id):
        """Ball olish"""
        uid = str(user_id)
        return self.data.get("users", {}).get(uid, {}).get("points", 0)
    
    # LANGUAGE
    def set_language(self, user_id, lang):
        """Til o'rnatish (uz/ru/en)"""
        self.data.setdefault("user_languages", {})[str(user_id)] = lang
        self.save()
    
    def get_language(self, user_id):
        """Foydalanuvchi tilini olish"""
        return self.data.get("user_languages", {}).get(str(user_id), "uz")
    
    # STATISTICS
    def get_top_rated_films(self, limit=10):
        """Eng yuqori baholangan filmlar"""
        film_ratings = []
        for film_key in self.data.get("ratings", {}).keys():
            avg = self.get_average_rating(film_key)
            count = self.get_rating_count(film_key)
            if avg and count >= 3:  # Kamida 3 ta baho
                film_ratings.append((film_key, avg, count))
        
        return sorted(film_ratings, key=lambda x: (x[1], x[2]), reverse=True)[:limit]
    
    def get_most_watched_films(self, limit=10):
        """Eng ko'p ko'rilgan filmlar"""
        film_counts = {}
        for history in self.data.get("watch_history", {}).values():
            for entry in history:
                film_key = entry["film_key"]
                film_counts[film_key] = film_counts.get(film_key, 0) + 1
        
        sorted_films = sorted(film_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_films[:limit]
    
    def get_top_users(self, limit=10):
        """Top foydalanuvchilar (points bo'yicha)"""
        users = []
        for uid, user_data in self.data.get("users", {}).items():
            users.append((
                int(uid),
                user_data.get("username"),
                user_data.get("first_name"),
                user_data.get("points", 0),
                user_data.get("videos_watched", 0)
            ))
        
        return sorted(users, key=lambda x: x[3], reverse=True)[:limit]
