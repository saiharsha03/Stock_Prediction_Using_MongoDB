#import necessary modules and packages
import keys
from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd

def connect_to_DB(database = "stock_data"):
    """
    Connects to the MongoDB database and returns the collection.
    
    Args:
        database (str): Name of the database to connect to.
        
    Returns:
        collection: MongoDB collection object.
    """
    client = MongoClient(keys.MONGO_URI)
    db = client['Stock_Prices']
    collection = db[database]
    return collection

def insert_to_DB(messages):
    """
    Inserts messages into the MongoDB database.
    
    Args:
        messages (list): List of dictionaries containing data to be inserted.
    """
    collection = connect_to_DB()
    try:
        collection.insert_many(messages, ordered=False) #Ordered=False to not break oon error
    except Exception as e:
          print("Error")

def get_latest_date():
    """
    Gets the latest date from the MongoDB database.
    
    Returns:
        str: Latest date in string format.
        str: Yesterday's date in string format.
        str: Today's date in string format.
    """
    collection = connect_to_DB()
    yesterday_date = datetime.now() - timedelta(days=1)
    if yesterday_date.weekday() == 5: 
        yesterday_date -= timedelta(days=1)
    elif yesterday_date.weekday() == 6:
        yesterday_date -= timedelta(days=2)
    yesterday_date_str = yesterday_date.strftime("%Y-%m-%d") 
    last_record= collection.find_one(sort=[("date", -1)])
    try:
        x = last_record["date"]
    except:
        x = "2023-01-09"
    today = datetime.now()
    today = today.strftime("%Y-%m-%d")
    return x,yesterday_date_str,today

def fetch_data():
    """
    Fetches all data from the MongoDB database and returns as a DataFrame.
    
    Returns:
        DataFrame: DataFrame containing all data from the database.
    """
    collection = connect_to_DB()
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    return df

def fetch_actual_prices(symbol):
    """
    Fetches actual prices for the given symbol from the MongoDB database.
    
    Args:
        symbol (str): Stock symbol.
        
    Returns:
        DataFrame: DataFrame containing actual prices for the given symbol.
    """
    collection = connect_to_DB()
    query = {'Symbol': symbol}
    results = collection.find(query)
    cleaned_results = [{key: result[key] for key in result if key in ['close', 'date']} for result in results]
    df = pd.DataFrame(cleaned_results)
    return df

def fetch_predicted_prices(symbol):
    """
    Fetches predicted prices for the given symbol from the MongoDB database.
    
    Args:
        symbol (str): Stock symbol.
        
    Returns:
        DataFrame: DataFrame containing predicted prices for the given symbol.
    """
    collection = connect_to_DB(database="predicted_prices")
    query = {'Symbol': symbol}
    results = collection.find(query)
    cleaned_results = [{key: result[key] for key in result if key not in ['_id', 'Symbol']} for result in results]
    df = pd.DataFrame(cleaned_results)
    return df