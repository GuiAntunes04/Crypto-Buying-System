from pymongo import MongoClient
import os

uri = os.getenv("MONGO_URI")

print("Tentando conectar...")
client = MongoClient(uri, serverSelectionTimeoutMS=3000)
client.admin.command("ping")
print("Conectou!")
