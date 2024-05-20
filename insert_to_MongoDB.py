import requests
from datetime import datetime, timedelta
import time
from pymongo import MongoClient
import streamlit as st

def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).date().isoformat()

     
def create_unique_index(collection):
    collection.create_index(
        [("date", 1), ("Symbol", 1)],
        unique=True
    )

def main():
    stocks =["IBM","AAPL", "TSLA", "META", "AMZN", "GOOGL", "CRM", "NVDA", "TSM", "WMT", "NFLX", "ACN", "MCD", "HSBC", "UBER"]
    base_url = "https://api.polygon.io/v2/aggs/ticker/"
    api_key = "4VpZC9HdYhwuH7TYsCghUSBqQxOprpvr"
    yesterday = datetime.now() - timedelta(1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    client = MongoClient('mongodb+srv://saiharsharudra03:hP86SW589uuV84K@stock.txb5u4z.mongodb.net/')
    db = client['your_database']
    collection = db['stock_data']
    create_unique_index(collection)
    messages = []
    last_record = collection.find_one({"Symbol": "IBM"},sort=[("date", -1)])
    print(last_record)    
    try:
         x = last_record["date"]
    except:
         x = "2023-01-09"
    if x == yesterday:
            st.write("Latest Data already present")
            return
    for stock in stocks:
        print(stock)
        time.sleep(20)
        url = f"{base_url}{stock}/range/1/day/{x}/{yesterday}?adjusted=true&sort=asc&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()
        for result in data["results"]:
            message = {
                    "Symbol": stock,
                    'date': convert_timestamp_to_date(result['t']),
                    'open': result['o'],
                    'high': result['h'],
                    'low': result['l'],
                    'close': result['c'],
                    'volume': result['v']
            }
            messages.append(message)
    if messages:
            collection.insert_many(messages)
main()