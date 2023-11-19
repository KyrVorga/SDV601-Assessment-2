from dotenv import load_dotenv
import os
import uuid
from .database import Database
import sys
sys.dont_write_bytecode = True

load_dotenv()


class DataExplorer:

    db = Database.getInstance()

    def __init__(self, name, username, _id=None, data=None, is_public=False, chat=None):
        """Initializes a DES object"""
        self._id = _id if _id else uuid.uuid4().hex
        self.name = name
        self.username = username
        self.data = data
        self.is_public = is_public
        self.chat = chat if chat else []

    def save(self):
        """Saves the data explorer to the database"""
        try:
            data_explorers = self.db.get_collection("data_explorers")

            data_explorer = {
                "name": self.name,
                "username": self.username,
                "data": self.data,
                "is_public": self.is_public,
                "chat": self.chat,
            }
            print("Data Explorer Save:", data_explorer)
            result = data_explorers.update_one(
                {"_id": self._id},
                {"$set": data_explorer},
                upsert=True
            )
            print("Data Explorer Save Result:", result)

        except Exception as e:
            print("Data Explorer Save Error:", e)

    def refresh(self):
        """Refreshes the data explorer from the database"""
        try:
            data_explorers = self.db.get_collection("data_explorers")

            data_explorer = data_explorers.find_one({"_id": self._id})

            if data_explorer:
                self.name = data_explorer["name"]
                self.username = data_explorer["username"]
                self.data = data_explorer["data"]
                self.is_public = data_explorer["is_public"]
                self.chat = data_explorer["chat"]

        except Exception as e:
            print("Data Explorer Refresh Error:", e)

    def delete(self):
        """Deletes the data explorer from the database"""
        try:
            data_explorers = self.db.get_collection("data_explorers")

            data_explorers.delete_one({"_id": self._id})

        except Exception as e:
            print("Data Explorer Delete Error:", e)

    def toggle_public(self, state):
        """Makes the data explorer public"""
        try:
            data_explorers = self.db.get_collection("data_explorers")

            data_explorers.update_one(
                {"_id": self._id},
                {"$set": {"is_public": state}}
            )

        except Exception as e:
            print("Data Explorer Make Public Error:", e)

    @classmethod
    def find_by_des_id(cls, _id):
        """Finds a data explorer by its _id"""
        try:
            data_explorers = cls.db.get_collection("data_explorers")

            data_explorer = data_explorers.find_one({"_id": _id})

            if data_explorer:
                return cls(
                    name=data_explorer["name"],
                    username=data_explorer["username"],
                    _id=data_explorer["_id"],
                    data=data_explorer["data"],
                    is_public=data_explorer["is_public"],
                    chat=data_explorer["chat"]
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
            data_explorers = cls.db.get_collection("data_explorers")

            data_explorer = data_explorers.find_one({"name": name})

            if data_explorer:
                return cls(
                    name=data_explorer["name"],
                    username=data_explorer["username"],
                    _id=data_explorer["_id"],
                    data=data_explorer["data"],
                    is_public=data_explorer["is_public"],
                    chat=data_explorer["chat"]
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
            data_explorers = cls.db.get_collection("data_explorers")

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
            data_explorers = cls.db.get_collection("data_explorers")

            data_explorer = data_explorers.find_one({"name": des_name})

            if data_explorer:
                return True
            else:
                return False

        except Exception as e:
            print("Data Explorer Find Error:", e)
            return None

    def __str__(self) -> str:
        return f"Data Explorer: {self.name} User:{self.username} ID:{self._id} Data:{self.data} Public:{self.is_public}"
