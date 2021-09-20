import os
from pymongo import MongoClient, GEOSPHERE


MONGO_DATABASE_URL: str = os.getenv("MONGO_CALCULUS_DATABASE_URL")

mongoclient = MongoClient(
    MONGO_DATABASE_URL,
    uuidRepresentation='standard'
)

partners_db = mongoclient.local.partners
partners_db.create_index([("coverageArea", GEOSPHERE)])
partners_db.create_index([("address", GEOSPHERE)])
