#import required libraries and functions
import requests
import time
import keys
from Database_Operations import insert_to_DB,get_latest_date
from Data_Processing import parse_result

def main():
    """
    Main function to fetch stock data from the Polygon API and insert into the database.
    """
    
    stocks =["IBM","AAPL", "TSLA", "META", "AMZN", "GOOGL", "CRM", "NVDA", "TSM", "WMT", "NFLX", "ACN", "MCD", "HSBC", "UBER"]
    base = "https://api.polygon.io/v2/aggs/ticker/"
    api = keys.API_KEY
    messages = []
    last_record,yesterday_date_str,today = get_latest_date()
    if (last_record == yesterday_date_str):
            return    
    for stock in stocks:
        url = f"{base}{stock}/range/1/day/{last_record}/{today}?adjusted=true&sort=desc&apiKey={api}"
        print(url)
        response = requests.get(url)
        data = response.json()
        for result in data["results"]:
            message = parse_result(result,stock)
            messages.append(message)
        time.sleep(20) #To avoid rate limiting. Polygon API allows only 5 calls per minute.
    if messages:
         insert_to_DB(messages)
if __name__ == '__main__':
    main()
