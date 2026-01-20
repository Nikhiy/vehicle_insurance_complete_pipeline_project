import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import MyException
from src.constants import DATABASE_NAME

class Proj1Data():
    """ 
    a class to mongodb records as a pandas dataframe
    """
    def __init__(self)->None:
        """
        Initializes the MongoDB client connection.
        """
        try:
            self.mongo_client=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e,sys)
        
    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            #accessing the collection from the default or specified databse_name
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection=self.mongo_client[database_name][collection_name]
            print("fetching data from mongodb")
            #converting the collection data to pd.dataframe and preprocess it
            df=pd.DataFrame(list(collection.find()))
            print(f"data fetched with len{len(df)}")
            if id in df.columns.to_list():
                df.drop(["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MyException(e,sys)