import os

from pymongo import MongoClient, ASCENDING


MONGO_DATABASE_URL: str = os.getenv("MONGO_PARTNERS_DATABASE_URL")

mongoclient = MongoClient(
    MONGO_DATABASE_URL,
    uuidRepresentation='standard'
)

partners_db = mongoclient.local.partners
partners_db.create_index([("id", ASCENDING)], unique=True)
partners_db.create_index([("document", ASCENDING)], unique=True)
