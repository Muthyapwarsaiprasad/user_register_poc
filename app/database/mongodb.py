from pymongo import MongoClient
from app.config.settings import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["user_db"]
users = db["users"]

# also collection to store password reset tokens/tracking:
tokens = db["reset_tokens"]