from dotenv import load_dotenv
import os
import uuid
from .database import Database
import sys
sys.dont_write_bytecode = True

load_dotenv()


class DataSource:

    db = Database.getInstance()

    def __init__(self, name, username, id, data):
        """Initializes a Data Source object"""
        self._id = id if id else uuid.uuid4().hex
        self.name = name
        self.username = username
        self.data = data

    def save(self):
        """Saves the data source to the database"""
        try:
            data_sources = self.db.get_collection("data_sources")

            data_source = {
                "name": self.name,
                "username": self.username,
                "data": self.data,
            }
            print("Data Source Save:", data_source)
            result = data_sources.update_one(
                {"_id": self._id},
                {"$set": data_source},
                upsert=True
            )
            print("Data Source Save Result:", result)

        except Exception as e:
            print("Data Source Save Error:", e)

    def refresh(self):
        """Refreshes the data source from the database"""
        try:
            data_sources = self.db.get_collection("data_sources")

            data_source = data_sources.find_one({"_id": self._id})

            if data_source:
                self.name = data_source["name"]
                self.username = data_source["username"]
                self.data = data_source["data"]

        except Exception as e:
            print("Data Source Refresh Error:", e)

    def delete(self):
        """Deletes the data source from the database"""
        try:
            data_sources = self.db.get_collection("data_sources")

            data_sources.delete_one({"_id": self._id})

        except Exception as e:
            print("Data Source Delete Error:", e)

    @classmethod
    def find_by_id(cls, id):
        """Returns a data source object with the given id"""
        try:
            data_sources = cls.db.get_collection("data_sources")
            data_source = data_sources.find_one({"_id": id})

            if data_source:
                return cls(data_source["name"], data_source["username"], data_source["_id"], data_source["data"])
            else:
                return None

        except Exception as e:
            print("Find Error:", e)
            return False

    @classmethod
    def find_by_name(cls, name):
        """Returns a data source object with the given name"""
        try:
            data_sources = cls.db.get_collection("data_sources")
            data_source = data_sources.find_one({"name": name})

            if data_source:
                return cls(data_source["name"], data_source["username"], data_source["_id"], data_source["data"])
            else:
                return None

        except Exception as e:
            print("Find Error:", e)
            return False

    @classmethod
    def find_by_username(cls, username):
        """Returns a data source object with the given username"""
        try:
            data_sources = cls.db.get_collection("data_sources")
            data_source = data_sources.find({"username": username})

            if data_source:
                return data_source
            else:
                return None

        except Exception as e:
            print("Find Error:", e)
            return False
