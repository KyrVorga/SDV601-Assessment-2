from datetime import datetime
from pymongo import MongoClient
from .database import Database

client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']


class Session:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token
        self.created_at = datetime.now()

    def save(self):
        sessions = db.sessions
        session_data = {
            'user_id': self.user_id,
            'token': self.token,
            'created_at': self.created_at
        }
        session_id = sessions.insert_one(session_data).inserted_id
        return session_id
