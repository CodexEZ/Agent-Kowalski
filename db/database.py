from motor.motor_asyncio import AsyncIOMotorClient


import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')

class AsyncMongoClient:

    @staticmethod
    def serialize_doc(doc):
        if not doc:
            return
        doc["_id"] = str(doc["_id"])
        return doc

    def __init__(self, db_name:str):
        client = AsyncIOMotorClient(MONGO_URL)
        self.db = client[db_name]
