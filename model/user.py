from .database import Database
import bcrypt
import os
from dotenv import load_dotenv
from .database import Database


class User:
    load_dotenv()

    db = Database(os.getenv('MONGO_URI'))

    def __init__(self, username, password, is_logged_in=False):
        """Initializes a user object"""

        # If the password is not encoded, encode it
        if type(password) == str:
            # Encode the password
            password_encoded = password.encode('utf-8')

            # Add the salt
            salt = bcrypt.gensalt()

            # Hash the password
            hashed = bcrypt.hashpw(password_encoded, salt)

            self.password = hashed
        else:
            self.password = password

        self.username = username
        self.is_logged_in = is_logged_in

    def check_password(self, password):
        '''Checks if the password provided matches the stored one'''
        try:
            password_encoded = password.encode('utf-8')
            return bcrypt.checkpw(password_encoded, self.password)

        except Exception as e:
            print('PW Check Error:', e)
            return False

    def save(self):
        """Saves the user to the database"""
        try:
            users = self.db.get_collection('mydatabase', 'users')

            user = {
                'username': self.username,
                'password': self.password,
                'is_logged_in': self.is_logged_in,
            }

            users.update_one(
                {'username': self.username},
                {'$set': user},
                upsert=True,
            )

        except Exception as e:
            print('Save Error:', e)
            return False

    @classmethod
    def find_by_username(cls, username):
        """Returns a user object with the given username"""
        try:
            users = cls.db.get_collection('mydatabase', 'users')
            user = users.find_one({'username': username})

            if user:
                return cls(user['username'], user['password'], user['is_logged_in'])
            else:
                return None

        except Exception as e:
            print('Find Error:', e)
            return False
