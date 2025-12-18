from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

market_logs = db.market_logs
