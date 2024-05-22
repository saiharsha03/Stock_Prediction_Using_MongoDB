#import necessary modules and functions
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from datetime import timedelta
from keras.layers import LSTM, Dense
from Database_Operations import connect_to_DB
import os 

def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

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
        data = data.sort_values(by='date')
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.drop('Symbol', axis=1, inplace=True)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df.values)
        time_step = 1
        X_train, y_train = create_dataset(scaled_data, time_step)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=100, batch_size=32)
        last_data = scaled_data[-time_step:]
        next_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=15, freq='D')
        predicted_prices = []
        for i in range(15):
            last_data = np.reshape(last_data, (1, time_step, 1))
            prediction = model.predict(last_data)
            predicted_prices.append(prediction[0][0])
            last_data = np.append(last_data[:, 1:, :], prediction.reshape(1, 1, 1), axis=1)
        predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))
        predicted_df = pd.DataFrame(predicted_prices, index=next_dates, columns=['Predicted_Value'])
        predicted_df['date'] = next_dates
        forecast_df = predicted_df[[ 'date', 'Predicted_Value']]
        forecast_df["Symbol"]=ticker
        collection1 = connect_to_DB(database= "predicted_prices")
        forecast_data = forecast_df.to_dict(orient='records')
        collection1.insert_many(forecast_data)

if __name__ == '__main__':
    LSTM_Model()