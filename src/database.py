import os
from pymongo import MongoClient
from dotenv import load_dotenv
import yaml

load_dotenv()

class MongoDB:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        if mongo_uri:
            self.client = MongoClient(mongo_uri)
            self.db = self.client.ecommerce
        else:
            raise ValueError("MONGO_URI not found in environment variables")

    def insert_item(self, collection_name, item):
        collection = self.db[collection_name]
        collection.insert_one(item)

    def close(self):
        self.client.close()


def get_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)
