import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from datetime import datetime,timedelta

def fetch_data():
    client = MongoClient('mongodb+srv://saiharsharudra03:hP86SW589uuV84K@stock.txb5u4z.mongodb.net/')
    db = client['your_database']
    collection = db['stock_data']
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    return df

def preprocess_data(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return scaler.fit_transform(df[['close']]), scaler

def create_sequences(data, sequence_length):
    sequences = []
    for i in range(len(data) - sequence_length):
        sequence = data[i:i+sequence_length]
        target = data[i+sequence_length]
        sequences.append((sequence, target))
    return sequences

def build_lstm_model(sequence_length):
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model, X_train, y_train, epochs, batch_size):
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)

def predict_future_prices(model, last_sequence, scaler, num_days):
    predicted_prices = []
    for _ in range(num_days):
        prediction = model.predict(last_sequence.reshape(1, last_sequence.shape[0], 1))
        predicted_prices.append(prediction[0, 0])
        last_sequence = np.append(last_sequence[1:], prediction[0, 0])
    predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))
    return predicted_prices

def store_predicted_prices(symbol, predicted_prices):
    client = MongoClient('mongodb+srv://saiharsharudra03:hP86SW589uuV84K@stock.txb5u4z.mongodb.net/')
    db = client['your_database']
    collection = db['predicted_prices']
    
    # Get today's date without time as a string
    today_date = datetime.today().date().strftime('%Y-%m-%d')
    
    # Iterate over each predicted price and store it as a separate document
    for idx, price in enumerate(predicted_prices, 1):
        # Calculate the date for this prediction
        prediction_date = (datetime.today().date() + timedelta(days=idx)).strftime('%Y-%m-%d')
        
        # Store the symbol, date, and predicted price
        data = {'symbol': symbol, 'date': prediction_date, 'predicted_price': price.item()}
        collection.insert_one(data)



def main():
    df = fetch_data()
    symbols = df['Symbol'].unique()

    for symbol in symbols:
        symbol_data = df[df['Symbol'] == symbol]
        data, scaler = preprocess_data(symbol_data)
        sequence_length = 30
        sequences = create_sequences(data, sequence_length)
        X_train = np.array([seq[0] for seq in sequences])
        y_train = np.array([seq[1] for seq in sequences])

        model = build_lstm_model(sequence_length)
        epochs = 50
        batch_size = 64
        train_model(model, X_train, y_train, epochs, batch_size)

        last_sequence = X_train[-1]
        predicted_prices = predict_future_prices(model, last_sequence, scaler, num_days=15)
        
        store_predicted_prices(symbol, predicted_prices)

if __name__ == '__main__':
    main()
