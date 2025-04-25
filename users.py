import json
import os

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()

    def load_users(self):
        """Загружает пользователей из JSON файла"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"users": [], "admins": []}
        return {"users": [], "admins": []}

    def save_users(self):
        """Сохраняет пользователей в JSON файл"""
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def register_user(self, username, is_admin=False):
        """Регистрирует нового пользователя"""
        if username in self.users["users"] or username in self.users["admins"]:
            return False, "Пользователь с таким именем уже существует"
        
        if is_admin:
            self.users["admins"].append(username)
        else:
            self.users["users"].append(username)
        
        self.save_users()
        return True, "Пользователь успешно зарегистрирован"

    def authenticate_user(self, username):
        """Проверяет существование пользователя и возвращает его роль"""
        if username in self.users["admins"]:
            return True, "admin"
        elif username in self.users["users"]:
            return True, "user"
        return False, None

    def get_all_users(self):
        """Возвращает списки всех пользователей и администраторов"""
        return self.users["users"], self.users["admins"] 