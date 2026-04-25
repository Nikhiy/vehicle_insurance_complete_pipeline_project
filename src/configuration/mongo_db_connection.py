import pymongo
import certifi
from typing import Optional
from src.constants import DATABASE_NAME, MONGODB_URL_KEY
from src.exception import MyException
from src.logger import logging
import os, sys

ca = certifi.where()

class MongoDBClient:
    client = None
    
    def __init__(self, database_name: Optional[str] = None):
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise MyException("Environment variable MONGODB_URL not set", sys)
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.database = MongoDBClient.client[database_name] if database_name else MongoDBClient.client[DATABASE_NAME]
            self.database.command("ping")
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise MyException(e, sys)

