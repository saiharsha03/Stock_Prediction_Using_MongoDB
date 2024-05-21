from datetime import datetime, timedelta

#This function is needed as API response returns data in epoch instead of actual timestamp

def convert_timestamp_to_date(timestamp):
    """
    Convert timestamp to date in ISO format.
    
    Args:
        timestamp (int): Timestamp value.
        
    Returns:
        str: Date in ISO format.
    """
    return datetime.fromtimestamp(timestamp / 1000).date().isoformat()

def parse_result(result,stock):
    """
    Parse the API result into a dictionary.
    
    Args:
        result (dict): Result from API response.
        stock (str): Stock symbol.
        
    Returns:
        dict: Parsed message containing stock data.
    """
    message = {
                    "Symbol": stock,
                    'date': convert_timestamp_to_date(result['t']),
                    'open': result['o'],
                    'high': result['h'],
                    'low': result['l'],
                    'close': result['c'],
                    'volume': result['v']
            }
    return message