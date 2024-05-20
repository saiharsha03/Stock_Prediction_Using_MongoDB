_**Deployed at: https://stock-predictions1.streamlit.app/**_

This project uses PolygonAPI to retrieve stock price information for 15 major tickes
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

Using Polygon API< the stock prices are retrieved in base.py file. 
Following this multiple functions are written to parse the output of API into proper format to store it in a MONGODB Database.
Following this a LSTM model was created to predict the price of each stock over next 15 days. 

A check was implemented to run the LSTM Model for every 7 days and when a new iteration of LSTM Model is run, the previously predicted data is erased to manage the storage space. MONGODB was chosen as the database for this project as it allows a free tier and db operations can be performed directly on the cloud. 

