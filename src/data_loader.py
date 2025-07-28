from tiingo import TiingoClient
import pandas as pd

def fetch_data_tiingo(ticker: str, api_key: str, start_date: str = '2015-01-01', end_date: str = '2024-12-31') -> pd.DataFrame:
    """
    Fetch adjusted OHLCV data from Tiingo.

    :param ticker: e.g., 'XLE'
    :param api_key: Your Tiingo API key
    :param start_date: Start date in YYYY-MM-DD
    :param end_date: End date in YYYY-MM-DD
    :return: DataFrame with datetime index and adjusted OHLCV columns
    """
    config = {
        'session': True,
        'api_key': api_key
    }
    client = TiingoClient(config)

    data = client.get_dataframe(
        ticker,
        startDate=start_date,
        endDate=end_date,
        frequency='daily'
    )

    # Standardize column names
    df = data.rename(columns={
        'adjOpen': 'Open',
        'adjHigh': 'High',
        'adjLow': 'Low',
        'adjClose': 'Adj Close',
        'adjVolume': 'Volume'
    })

    df = df[['Open', 'High', 'Low', 'Adj Close', 'Volume']]
    df['Close'] = df['Adj Close']  # For compatibility with your backtester
    df.index.name = 'Date'

    return df
