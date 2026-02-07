#!/usr/bin/env python3
# GitHub push script - PyGithub orqali

import os
import json
from github import Github, GithubException

# GitHub ma'lumotlari
USERNAME = "farruhjohonboyev9-wq"
REPO_NAME = "filimuz-bot"
TOKEN = "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"

# Yuklash uchun fayllar
FILES_TO_UPLOAD = [
    "filimuz.py",
    "config.py",
    "database.py",
    "database.json",
    "films_database.json",
    "requirements.txt",
    "Procfile",
    "runtime.txt",
    "DEPLOYMENT.md",
]

def push_to_github(token, username, repo_name, files):
    """GitHub ga fayllarni push qilish"""
    try:
        # GitHub ga ulanish
        print(f"🔗 GitHub ga ulanilmoqda ({username})...")
        g = Github(token)
        user = g.get_user()
        
        # Repository oling
        try:
            repo = user.get_repo(repo_name)
            print(f"✅ Repository topildi: {repo.html_url}")
        except GithubException as e:
            print(f"❌ Repository topilmadi: {repo_name}")
            print(f"GitHub da qo'lda yarating: https://github.com/new")
            return False
        
        # Fayllarni yuklash
        print(f"\n📤 {len(files)} ta fayl yuklanmoqda...\n")
        
        for file_name in files:
            file_path = os.path.join(os.getcwd(), file_name)
            
            if not os.path.exists(file_path):
                print(f"⚠️  {file_name} topilmadi, skip...")
                continue
            
            try:
                # Fayl o'qish
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Tekshirish - fayl GitHub da bor-yo'q
                try:
                    existing = repo.get_contents(file_name)
                    # Update existing file
                    repo.update_file(
                        path=file_name,
                        message=f"Update {file_name}",
                        content=content,
                        sha=existing.sha
                    )
                    print(f"✏️  {file_name} yangilandi")
                except GithubException:
                    # Create new file
                    repo.create_file(
                        path=file_name,
                        message=f"Add {file_name}",
                        content=content
                    )
                    print(f"✅ {file_name} yuklandi")
            
            except Exception as e:
                print(f"❌ {file_name}: {str(e)}")
        
        print(f"\n✨ Tayyoq! Repository: {repo.html_url}")
        print(f"🚀 Railway.app ga deploy qilishga tayyoq!")
        
        return True
    
    except Exception as e:
        print(f"❌ Xato: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 FILIMUZ BOT - GITHUB PUSH")
    print("="*40)
    
    push_to_github(TOKEN, USERNAME, REPO_NAME, FILES_TO_UPLOAD)
