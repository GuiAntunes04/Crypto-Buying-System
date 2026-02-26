import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db_client():
    uri = os.getenv("MONGO_URI")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        print("✅ Conectado ao MongoDB Atlas")
        return client
    except Exception as e:
        print(f"❌ Erro ao conectar no MongoDB: {e}")
        return None
