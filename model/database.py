from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import sys
sys.dont_write_bytecode = True


class Database:
    def __init__(self, uri):
        self.client = MongoClient(uri, server_api=ServerApi("1"))
        try:
            self.client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def get_collection(self, db_name, collection_name):
        db = self.client[db_name]
        return db[collection_name]
