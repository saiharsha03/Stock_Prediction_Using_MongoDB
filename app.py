import streamlit as st
from pymongo import MongoClient
import pandas as pd
import numpy as np
from insert_to_MongoDB import main as fetch_new_data
def fetch_data():
    client = MongoClient('mongodb+srv://saiharsharudra03:hP86SW589uuV84K@stock.txb5u4z.mongodb.net/')
    db = client['your_database']
    collection = db['stock_data']
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    return df
def fetch_latest():
     with st.spinner("Fetching New Data"):
         fetch_new_data()

def fetch_predicted_prices(symbol):
    client = MongoClient('mongodb+srv://saiharsharudra03:hP86SW589uuV84K@stock.txb5u4z.mongodb.net/')
    db = client['your_database']
    collection = db['predicted_prices']
    query = {'symbol': symbol}
    results = collection.find(query)
    predicted_prices = [result['predicted_price'] for result in results] if results else None
    return predicted_prices


def filter_data(df, symbol):
    return df[df['Symbol'] == symbol]

def main():
    st.title('Stock Closing Rates Variation')
    fetch_latest()
    df = fetch_data()
    symbols = df['Symbol'].unique()
    selected_symbol = st.selectbox('Select Symbol', symbols)
    filtered_data = filter_data(df, selected_symbol)
    
    st.line_chart(filtered_data.set_index('date')['close'], use_container_width=True)

    predicted_prices = fetch_predicted_prices(selected_symbol)
    if predicted_prices:
        st.header('Predicted Prices for Next 15 Days')
        # Convert predicted prices to DataFrame
        dates = pd.date_range(start=filtered_data['date'].iloc[-1], periods=16)[1:]
        predicted_data = pd.DataFrame({'date': dates, 'predicted_prices': predicted_prices})
        st.line_chart(predicted_data.set_index('date'), use_container_width=True)
    else:
        st.warning("No predicted prices available for the selected symbol.")

if __name__ == '__main__':
    main()
