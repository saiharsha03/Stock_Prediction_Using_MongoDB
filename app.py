#Import Necessary Modules and Functions
import streamlit as st
import pandas as pd
from Base import main as fetch_new_data
import matplotlib.pyplot as plt
from Database_Operations import fetch_data,fetch_actual_prices,fetch_predicted_prices
from lstm_check import update_metadata_date

fetch_executed = True

def fetch_latest():
    """
    Fetches the latest data and updates the Streamlit app interface.
    """
    empty_placeholder = st.empty()
    empty_placeholder.write("Fetching New Data...")
    empty_placeholder.image("loading.gif")
    fetch_new_data()
    empty_placeholder.empty()

def merge_data(predicted_df, actual_df):
    """
    Merges predicted and actual dataframes on the date column.
    
    Args:
        predicted_df (DataFrame): DataFrame containing predicted prices.
        actual_df (DataFrame): DataFrame containing actual prices.

    Returns:
        DataFrame: Merged DataFrame.
    """
    merged_df = pd.merge(predicted_df, actual_df, on='date', how='left')
    return merged_df

def filter_data(df, symbol):
    """
    Filters the DataFrame based on the selected symbol.
    
    Args:
        df (DataFrame): DataFrame to be filtered.
        symbol (str): Selected symbol.

    Returns:
        DataFrame: Filtered DataFrame.
    """
    return df[df['Symbol'] == symbol]

def main():
    """
    Main function to display the Streamlit app interface.
    """
    st.title('Stock Closing Rates Variation')
    df = fetch_data()
    update_metadata_date()
    symbols = df['Symbol'].unique()
    selected_symbol = st.selectbox('Select Symbol', symbols)
    filtered_data = filter_data(df, selected_symbol)
    st.line_chart(filtered_data.set_index('date')['close'], use_container_width=True)
    df1 = fetch_predicted_prices(selected_symbol)
    df1['date'] = pd.to_datetime(df1['date']).dt.strftime('%Y-%m-%d') 
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
