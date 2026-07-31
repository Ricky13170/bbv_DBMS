import os
import json
from django.conf import settings

class AuthRepository:
    @staticmethod
    def _get_file_path():
        return os.path.join(settings.BASE_DIR, 'data.json')

    @staticmethod
    def get_user_by_username(username):
        file_path = AuthRepository._get_file_path()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                users_db = json.load(f)
        except Exception:
            return None
            
        for u in users_db:
            if u.get('username') == username:
                return u
        return None

    @staticmethod
    def get_all_users():
        file_path = AuthRepository._get_file_path()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def save_user(new_user):
        users_db = AuthRepository.get_all_users()
        users_db.append(new_user)
        
        file_path = AuthRepository._get_file_path()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(users_db, f, indent=4)
        return True
