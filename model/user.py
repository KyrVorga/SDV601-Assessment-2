from dotenv import load_dotenv
import os
import bcrypt
from .database import Database
import sys
sys.dont_write_bytecode = True

load_dotenv()


class User:

    db = Database.getInstance()

    def __init__(self, username, password, is_logged_in=False, session_id=None):
        """Initializes a user object"""

        # If the password is not encoded, encode it
        if type(password) == str:
            # Encode the password
            password_encoded = password.encode("utf-8")

            # Add the salt
            salt = bcrypt.gensalt()

            # Hash the password
            hashed = bcrypt.hashpw(password_encoded, salt)

            self.password = hashed
        else:
            self.password = password

        self.username = username
        self.is_logged_in = is_logged_in
        self.session_id = session_id

    def check_password(self, password):
        """Checks if the password provided matches the stored one"""
        try:
            password_encoded = password.encode("utf-8")
            return bcrypt.checkpw(password_encoded, self.password)

        except Exception as e:
            print("PW Check Error:", e)
            return False

    def save(self):
        """Saves the user to the database"""
        try:
            users = self.db.get_collection("users")

            user = {
                "username": self.username,
                "password": self.password,
                "is_logged_in": self.is_logged_in,
                "session_id": self.session_id,
            }

            users.update_one(
                {"username": self.username},
                {"$set": user},
                upsert=True,
            )

        except Exception as e:
            print("Save Error:", e)
            return False

    @classmethod
    def find_by_username(cls, username):
        """Returns a user object with the given username"""
        try:
            users = cls.db.get_collection("users")
            user = users.find_one({"username": username})

            if user:
                return cls(user["username"], user["password"], user["is_logged_in"], user["session_id"])
            else:
                return None

        except Exception as e:
            print("Find Error:", e)
            return False

    @classmethod
    def find_by_session_id(cls, session_id):
        """Returns a user object with the given session_id"""
        try:
            users = cls.db.get_collection("users")
            user = users.find_one({"session_id": session_id})

            if user:
                return cls(user["username"], user["password"], user["is_logged_in"], user["session_id"])
            else:
                return None

        except Exception as e:
            print("Find Error:", e)
            return False

    @classmethod
    def user_exists(cls, username):
        """Returns true if a user with the given username exists"""
        try:
            users = cls.db.get_collection("users")
            user = users.find_one({"username": username})

            if user:
                return True
            else:
                return False

        except Exception as e:
            print("Find Error:", e)
            return False
