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
