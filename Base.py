import requests
import time
import keys
from Database_Operations import connect_to_DB,insert_to_DB,get_latest_date
from Data_Processing import parse_result
import os

def main():
    stocks =["IBM","AAPL", "TSLA", "META", "AMZN", "GOOGL", "CRM", "NVDA", "TSM", "WMT", "NFLX", "ACN", "MCD", "HSBC", "UBER"]
    base_url = "https://api.polygon.io/v2/aggs/ticker/"
    api_key = keys.API_KEY
    messages = []
    last_record,yesterday_date_str,today = get_latest_date()
    if (last_record == yesterday_date_str):
            return    
    for stock in stocks:
        os.write("Fetching New Data")
        url = f"{base_url}{stock}/range/1/day/{last_record}/{today}?adjusted=true&sort=desc&apiKey={api_key}"
        os.write(url)
        response = requests.get(url)
        data = response.json()
        for result in data["results"]:
            message = parse_result(result,stock)
            messages.append(message)
            time.sleep(20)
    if messages:
         insert_to_DB(messages)
if __name__ == '__main__':
    main()
