from dotenv import load_dotenv
import os
import uuid
from .database import Database
import sys
sys.dont_write_bytecode = True

load_dotenv()


class DataExplorer:

    db = Database(os.getenv("MONGO_URI"))

    def __init__(self, name, username, des_id=None, data=None, is_public=False):
        """Initializes a user object"""

        self.name = name
        self.username = username
        if des_id == None:
            self.des_id = self.generate_des_id()
            print("Data Explorer ID:", self.des_id)
        self.des_id = des_id
        self.data = data
        self.is_public = is_public

    def save(self):
        """Saves the data explorer to the database"""
        try:
            data_explorers = self.db.get_collection(
                "mydatabase", "data_explorers")

            data_explorer = {
                "name": self.name,
                "username": self.username,
                "des_id": self.des_id,
                "data": self.data,
                "is_public": self.is_public,
            }
            print("Data Explorer Save:", data_explorer)
            data_explorers.update_one(
                {"des_id": self.des_id},
                {"$set": data_explorer},
                upsert=True
            )

        except Exception as e:
            print("Data Explorer Save Error:", e)

    def delete(self):
        """Deletes the data explorer from the database"""
        try:
            data_explorers = self.db.get_collection(
                "mydatabase", "data_explorers")

            data_explorers.delete_one({"des_id": self.des_id})

        except Exception as e:
            print("Data Explorer Delete Error:", e)

    def toggle_public(self, state):
        """Makes the data explorer public"""
        try:
            data_explorers = self.db.get_collection(
                "mydatabase", "data_explorers")

            data_explorers.update_one(
                {"des_id": self.des_id},
                {"$set": {"is_public": state}}
            )

        except Exception as e:
            print("Data Explorer Make Public Error:", e)

    @classmethod
    def find_by_des_id(cls, des_id):
        """Finds a data explorer by its des_id"""
        try:
            data_explorers = cls.db.get_collection(
                "mydatabase", "data_explorers")

            data_explorer = data_explorers.find_one({"des_id": des_id})

            if data_explorer:
                return cls(
                    name=data_explorer["name"],
                    username=data_explorer["username"],
                    des_id=data_explorer["des_id"],
                    data=data_explorer["data"],
                    is_public=data_explorer["is_public"]
                )
            else:
                return None

        except Exception as e:
            print("Data Explorer Find Error:", e)
            return None

    @classmethod
    def find_by_name(cls, name):
        """Finds a data explorer by its name"""
        try:
            data_explorers = cls.db.get_collection(
                "mydatabase", "data_explorers")

            data_explorer = data_explorers.find_one({"name": name})

            if data_explorer:
                return cls(
                    name=data_explorer["name"],
                    username=data_explorer["username"],
                    des_id=data_explorer["des_id"],
                    data=data_explorer["data"],
                    is_public=data_explorer["is_public"]
                )
            else:
                return None

        except Exception as e:
            print("Data Explorer Find Error:", e)
            return None

    @classmethod
    def find_available_des(cls, username):
        """Finds all data explorers that are available to the user"""
        try:
            data_explorers = cls.db.get_collection(
                "mydatabase", "data_explorers")

            available_des = data_explorers.find(
                {"$or": [{"username": username}, {"is_public": True}]})

            if available_des:
                return available_des
            else:
                return None

        except Exception as e:
            print("Data Explorer Find Error:", e)
            return None

    @classmethod
    def des_exists(cls, des_name):
        """Checks if a data explorer exists"""
        try:
            data_explorers = cls.db.get_collection(
                "mydatabase", "data_explorers")

            data_explorer = data_explorers.find_one({"name": des_name})

            if data_explorer:
                return True
            else:
                return False

        except Exception as e:
            print("Data Explorer Find Error:", e)
            return None

    @staticmethod
    def generate_des_id():
        """Generates a unique des_id"""
        return str(uuid.uuid4())
