from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
chicago_crash_db = client['chicago_crash']


crashes = chicago_crash_db['crashs']
