from pymongo import MongoClient
from dotenv import load_dotenv
import os 


load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

Client = MongoClient(MONGO_URL)

db = Client["User-Management"]

user_collection = db["users"]
