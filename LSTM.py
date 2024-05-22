#import necessary modules and functions
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense
from Database_Operations import connect_to_DB
import os 

def LSTM_Model():
    """
    Runs the LSTM model to predict stock prices and inserts the predicted prices into the database.
    """
    os.write(1,b"Running LSTM Model")
    collection = connect_to_DB()
    projection = {"_id": 0, "Symbol": 1, "date": 1, "close": 1}  # Include Ticker, Date, and Close fields
    cursor = collection.find({}, projection)
    df = pd.DataFrame(list(cursor))
    df['date'] = pd.to_datetime(df['date'])
    df['numerical_representation'] = df['date'].apply(lambda x: x.timestamp())
    df = df.sort_values(by='numerical_representation')
    tickers = df["Symbol"].unique().tolist()
    for ticker in tickers:
        data = df[df['Symbol'] == ticker]
        X = data['numerical_representation'].values.reshape(-1, 1)
        y = data['close'].values
        model = Sequential([
        LSTM(50, activation='relu', input_shape=(1, 1)),
        Dense(1)])
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=100, verbose=0)
        last_date_numeric = df['numerical_representation'].iloc[-1]
        forecast_dates_numeric = [last_date_numeric + i * 86400 for i in range(1, 16) if (last_date_numeric + i * 86400) % 86400 // 3600 // 24 % 7 not in (5, 6)]
        forecast_input = np.array([[date] for date in forecast_dates_numeric])
        forecast = model.predict(forecast_input).flatten()
        forecast_dates = pd.to_datetime(forecast_dates_numeric, unit='s')
        forecast_df = pd.DataFrame({'Date': forecast_dates, 'Predicted_Value': forecast})
        forecast_df['Symbol'] = ticker
        collection1 = connect_to_DB(database= "predicted_prices")
        forecast_data = forecast_df.to_dict(orient='records')
        collection1.insert_many(forecast_data)

if __name__ == '__main__':
    LSTM_Model()