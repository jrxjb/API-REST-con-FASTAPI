import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Cargar las variables del archivo .env al entorno del sistema
load_dotenv()

# Obtener las variables del entorno
MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Crear la conexión a MongoDB utilizando las variables de entorno
conn = MongoClient(MONGO_URL)
db = conn[DATABASE_NAME]
users_collection = db[COLLECTION_NAME]

# Ahora puedes usar `users_collection` en tu aplicación
