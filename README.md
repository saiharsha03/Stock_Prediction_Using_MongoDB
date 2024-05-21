_**Deployed at: https://stock-predictions1.streamlit.app/**_

This project utilizes Long Short-Term Memory (LSTM) neural networks to predict stock prices based on historical data. It includes functionalities for fetching data from a MongoDB database, training an LSTM model, and inserting predicted prices back into the database.

Components

Base/main.py: Python script for fetching new data from an external Polygon API and inserting it into the database.

Database_Operations.py: Module for database operations such as connecting to the database and fetching data.

keys.py: Module containing API keys and other sensitive information.

Data_Processing.py: Module for processing data, including parsing API responses and converting timestamps.

LSTM/update_metadata_date.py: Script to update metadata date and trigger LSTM model training.

LSTM/LSTM_Model.py: Script containing the LSTM model implementation and data insertion.

app.py: Streamlit application script for visualizing stock closing rates variation.

README.md: Markdown file providing an overview of the project and instructions for usage.

For the following stocks:

"IBM"  - IBM
"AAPL" - APPLE
"TSLA" - TESLA
"META" - META
"AMZN" - AMAZON
"GOOGL" - GOOGLE
"CRM" - SALESFORCE
"NVDA" - NVIDIA
"TSM" - TAIWAN SEMICONDUCTOR MANUFACTURING
"WMT" - WALMART
"NFLX" - NETFLIX
"ACN" - ACCENTURE
"MCD" - MCDONALDS
"HSBC" - HSBC BANK and
"UBER" - UBER. 

A check was implemented to run the LSTM Model for every 7 days and when a new iteration of LSTM Model is run, the previously predicted data is erased to manage the storage space. MONGODB was chosen as the database for this project as it allows a free tier and db operations can be performed directly on the cloud. 

