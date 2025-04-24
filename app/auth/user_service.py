import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
USER_FILE = 'users.json'

class UserService:
    def __init__(self):
        self.users = self._load_users()

    def _load_users(self):
        filepath = os.path.join(DATA_DIR, USER_FILE)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error decoding user data from {USER_FILE}.")
            return []


    def authenticate_user(self, username, password):
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return user['role']
        return None

    def get_user_role(self, username):
        for user in self.users:
            if user['username'] == username:
                return user['role']
        return None