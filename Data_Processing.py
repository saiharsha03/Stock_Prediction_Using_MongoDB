from datetime import datetime, timedelta

def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).date().isoformat()

def parse_result(result,stock):
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