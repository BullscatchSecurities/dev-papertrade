import json
import pandas as pd

from settings import REDIS_CLIENT




def getData(symbol, interval, exchange="NSE", nbars=100):
    """
    Fetch, parse, and return candle data from Redis as a Pandas DataFrame.

    Args:
        symbol (str): The symbol name (e.g., "NATURALGAS25JANFUT").
        interval (str): The time interval (e.g., "1minute", "5minute").
        exchange (str): The exchange name (e.g., "NSE", "MCX", "BSE").
        nbars (int): The number of recent bars to fetch.

    Returns:
        pd.DataFrame: A DataFrame containing the candle data with columns:
                    ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    """
    try:

        key = f"Interval:{interval}:{exchange}:{symbol}"
        raw_data = REDIS_CLIENT.lrange(key, -nbars, -1)
        candle_data = [json.loads(item) for item in raw_data]
        df = pd.DataFrame(candle_data)
        df.rename(columns={'date': 'timestamp'}, inplace=True)
        final_df = df.sort_values(by='timestamp').reset_index(drop=True)

        del df

        return final_df

    except Exception as e:
        print(f"Error fetching or processing data for symbol '{symbol}' and interval '{interval}': {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Example usage
# symbol = "NATURALGAS25JANFUT"
# interval = "1minute"
# Exchange = "MCX"
# nbars = 50  # Fetch the last 50 bars
# df = getData(symbol, interval,"MCX", nbars)
# print(df.head())
