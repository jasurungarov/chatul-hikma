import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["chatul_hikma"]
users = db["users"]

def init_db():
    users.create_index("chat_id", unique=True)

def save_user_to_db(user):
    if not users.find_one({"chat_id": user["chat_id"]}):
        users.insert_one(user)

def get_all_users():
    return list(users.find())

def get_user_by_chat_id(chat_id):
    return users.find_one({"chat_id": chat_id})