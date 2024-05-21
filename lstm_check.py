#mport necesssary modules
from pymongo import MongoClient
from datetime import datetime, timedelta
import keys
from LSTM import LSTM_Model

def update_metadata_date():
    """
    Updates the metadata date and triggers LSTM model training if necessary.
    """
    
    client = MongoClient(keys.MONGO_URI)
    db = client['metadata_DB']
    metadata_collection = db['metadata']
    predicted_prices_db = client['predicted_prices']
    metadata_doc = metadata_collection.find_one()
    today = datetime.now()
    if metadata_doc and metadata_doc.get('date'):
        stored_date = metadata_doc['date']
        if today - stored_date >= timedelta(days=7):
            metadata_collection.update_one({}, {"$set": {"date": today}})
            predicted_prices_db.delete_many({})
            LSTM_Model()
    else:
        metadata_collection.insert_one({"date": today})

    if not metadata_doc:
        LSTM_Model() 