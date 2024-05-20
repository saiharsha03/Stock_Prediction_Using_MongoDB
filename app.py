import streamlit as st
import pandas as pd
import numpy as np
from Base import main as fetch_new_data
from LSTM import LSTM_Model
import matplotlib.pyplot as plt
from Database_Operations import fetch_data,fetch_actual_prices,fetch_predicted_prices
from lstm_check import update_metadata_date

fetch_executed = True

def fetch_latest():
    empty_placeholder = st.empty()
    empty_placeholder.write("Fetching New Data...")
    # You can add your animation image here
    empty_placeholder.image("loading.gif")

    fetch_new_data()
    empty_placeholder.empty()
def merge_data(predicted_df, actual_df):
    merged_df = pd.merge(predicted_df, actual_df, on='date', how='left')
    return merged_df

def filter_data(df, symbol):
    return df[df['Symbol'] == symbol]

def main():
    st.title('Stock Closing Rates Variation')
    df = fetch_data()
    update_metadata_date()
    symbols = df['Symbol'].unique()
    selected_symbol = st.selectbox('Select Symbol', symbols)
    filtered_data = filter_data(df, selected_symbol)
    
    st.line_chart(filtered_data.set_index('date')['close'], use_container_width=True)

    df1 = fetch_predicted_prices(selected_symbol)
    df1['Date'] = pd.to_datetime(df1['Date']).dt.strftime('%Y-%m-%d') 
    df1.rename(columns={'Date': 'date'}, inplace=True)
    actual_df = fetch_actual_prices(selected_symbol)
    actual_df['date'] = pd.to_datetime(actual_df['date']).dt.strftime('%Y-%m-%d')  # Convert Date column to string format

    merged_df = merge_data(df1, actual_df)

    merged_df['close'] = merged_df['close'].fillna('Data not available')  # Fill missing actual prices with "Data not available"
    merged_df.rename(columns={'close': 'Actual_Price'}, inplace=True)
    st.line_chart(df1.set_index('date')["Predicted_Value"],use_container_width=True)
    st.subheader('Predicted Values')
    st.table(merged_df[['date', 'Predicted_Value', 'Actual_Price']])

if __name__ == '__main__':
    if fetch_executed:
        fetch_latest()
        fetch_executed = False
    main()
