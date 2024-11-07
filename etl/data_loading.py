import json
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os 

load_dotenv()

client = MongoClient(os.environ.get("MONGO_DB_URL"))  

db = client['BookRecommendations']
collection = db['Books']

# Load your clean data.
with open("data/goodreads_books_clean.json", 'r') as file:
    book_data = json.load(file)

if isinstance(book_data, list):
    collection.insert_many(book_data)
else:
    collection.insert_one(book_data)

print("Data uploaded successfully!")
