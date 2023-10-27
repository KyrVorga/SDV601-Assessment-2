from datetime import datetime
# from pymongo import MongoClient
from .database import Database
import bcrypt

# client = MongoClient('mongodb://localhost:27017/')
# db = client['mydatabase']


class User:
    db = Database(
        'mongodb+srv://KyrVorga:Alicization44@cluster0.fittcye.mongodb.net/?retryWrites=true&w=majority')

    def __init__(self, username, password):
        password_encoded = password.encode('utf-8')

        # Adding the salt to password
        salt = bcrypt.gensalt()
        # Hashing the password
        hashed = bcrypt.hashpw(password_encoded, salt)

        self.username = username
        self.password = hashed

    def save(self):
        users = self.db.get_collection('mydatabase', 'users')

        user_data = {
            'username': self.username,
            'password': self.password,
            'created_at': datetime.now()
        }
        user_id = users.insert_one(user_data).inserted_id
        self.id = user_id
        return user_id

    @classmethod
    def find_by_username(cls, username):
        users = cls.db.get_collection('mydatabase', 'users')
        user_data = users.find_one({'username': username})
        if user_data:
            return cls(user_data['username'], user_data['password'])
        else:
            return None
