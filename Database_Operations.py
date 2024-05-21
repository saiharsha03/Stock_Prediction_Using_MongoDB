import keys
from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd
import os

def connect_to_DB(database = "stock_data"):
    os.write("DB Connected")
    client = MongoClient(keys.MONGO_URI)
    db = client['Stock_Prices']
    collection = db[database]
    return collection

def insert_to_DB(messages):
    print("Inserting new Data")
    collection = connect_to_DB()
    try:
        collection.insert_many(messages, ordered=False)
    except Exception as e:
          print("Error")

def get_latest_date():
    collection = connect_to_DB()
    yesterday_date = datetime.now() - timedelta(days=1)
    if yesterday_date.weekday() == 5: 
        yesterday_date -= timedelta(days=1)
    elif yesterday_date.weekday() == 6:
        yesterday_date -= timedelta(days=2)
    yesterday_date_str = yesterday_date.strftime("%Y-%m-%d") 
    last_record= collection.find_one(sort=[("date", -1)])
    x = last_record["date"]
    today = datetime.now()
    today = today.strftime("%Y-%m-%d")
    return x,yesterday_date_str,today

def fetch_data():
    collection = connect_to_DB()
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    return df

def fetch_actual_prices(symbol):
    collection = connect_to_DB()
    query = {'Symbol': symbol}
    results = collection.find(query)
    cleaned_results = [{key: result[key] for key in result if key in ['close', 'date']} for result in results]
    df = pd.DataFrame(cleaned_results)
    return df

def fetch_predicted_prices(symbol):
    collection = connect_to_DB(database="predicted_prices")
    query = {'Symbol': symbol}
    results = collection.find(query)
    cleaned_results = [{key: result[key] for key in result if key not in ['_id', 'Symbol']} for result in results]
    df = pd.DataFrame(cleaned_results)
    return df