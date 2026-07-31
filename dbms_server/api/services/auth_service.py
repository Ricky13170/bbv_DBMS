from api.repositories.auth_repository import AuthRepository
from rest_framework_simplejwt.tokens import RefreshToken

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        user = AuthRepository.get_user_by_username(username)
        if user and user.get('password') == password:
            class FakeUser:
                def __init__(self, user_id):
                    self.id = user_id
                    self.pk = user_id
            user_obj = FakeUser(user['id'])
            refresh = RefreshToken.for_user(user_obj)
            return {
                "user_id": user['id'],
                "username": user['username'],
                "role": user.get('role', 'user'),
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        return None

    @staticmethod
    def register_user(username, password):
        user = AuthRepository.get_user_by_username(username)
        if user:
            return None 
            
        all_users = AuthRepository.get_all_users()
        new_id = 1 if len(all_users) == 0 else all_users[-1]['id'] + 1
        new_user = {
            "id": new_id,
            "username": username,
            "password": password,
            "role": "user"
        }
        
        AuthRepository.save_user(new_user)
        
        return {
            "id": new_user["id"],
            "username": new_user["username"],
            "role": new_user["role"],
            "message": "User created successfully!"
        }
