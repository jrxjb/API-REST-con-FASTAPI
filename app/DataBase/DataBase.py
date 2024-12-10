from pymongo import MongoClient

conn = MongoClient('mongodb://localhost:27017/')
db = conn['local']
users_collection = db['fastAPI_ejemplo1']