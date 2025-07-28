import pandas as pd

def sma_crossover_strategy(data: pd.DataFrame, short_window: int = 20, long_window: int = 50):
    """
    Generate signals based on SMA crossover strategy.
    Returns a DataFrame with signals.
    """
    df = data.copy()
    df['SMA_Short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['Close'].rolling(window=long_window).mean()
    df['Signal'] = 0
    df.loc[df['SMA_Short'] > df['SMA_Long'], 'Signal'] = 1
    df.loc[df['SMA_Short'] < df['SMA_Long'], 'Signal'] = -1
    df['Signal'] = df['Signal'].shift(1)  # Avoid lookahead bias
    return df   