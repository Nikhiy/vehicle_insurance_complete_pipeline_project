import os
import pymongo
import sys
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME,MONGODB_URL_KEY

#loading the certifcate authority file to avoid timeout errors while connectiong to mongodb
#it basically tells python which certificate is safe while connecting to https
ca=certifi.where()

class MongoDBClient():
    """
    this class is responsible for connectiong to mongodb database
    attributes:
        client:MongoClient
            a shared mongoclient for the class
        database:Database
            The specific database instance that MongoDBClient connects to.
    Methods:
    -------
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name.

    """
    client = None  # Shared MongoClient instance across all MongoDBClient instances
    #basically a instance like a class one only

    def __init__(self,database_name:str=DATABASE_NAME)->None:
        """
        Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

        Parameters:
        ----------
        database_name : str, optional
            Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

        Raises:
        ------
        MyException
            If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
        try:
            #check if mongodb connection is already there if not create a new one
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set")
                
                #estlablishing a new mongodb client connection
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

            #set this mongodb.client to our original client varaible
            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info('MONGODB CONNECTION SUCCESFULLY')
        except Exception as e:
            raise MyException(e,sys)

