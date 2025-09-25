# Minimal BotDatabase to get the bot running
# Stores data in memory. Replace with your full implementation later.

from typing import List, Dict

class BotDatabase:
    def __init__(self):
        self.users = {}
        self.history = {}

    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        self.users[user_id] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "verified": False
        }

    def verify_user(self, user_id: int):
        if user_id in self.users:
            self.users[user_id]["verified"] = True

    def add_conversation(self, user_id: int, role: str, content: str):
        self.history.setdefault(user_id, []).append({"role": role, "content": content})

    def clear_conversation(self, user_id: int):
        self.history[user_id] = []

    def get_enhanced_conversation_context(self, user_id: int) -> Dict:
        return {
            "conversation_history": self.history.get(user_id, [])
        }
