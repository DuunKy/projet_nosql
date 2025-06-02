from pymongo import MongoClient
import os

CLIENT = MongoClient(os.getenv("MONGO_URI"))
DATABASE = CLIENT.get_database(os.getenv("DB_NAME"))
