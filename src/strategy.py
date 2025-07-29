import pandas as pd
from ta.volatility import AverageTrueRange

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
    return df   

def add_atr_filter(df, atr_window=14, atr_ma_window=100):
    atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Adj Close'], window=atr_window)
    df['ATR'] = atr.average_true_range()
    df['ATR_Smooth'] = df['ATR'].rolling(window=atr_ma_window).mean()
    df['LowVol'] = df['ATR'] < df['ATR_Smooth']
    return df

def sma_crossover_with_atr_filter(df, short_window=20, long_window=50):
    df = df.copy()
    df['SMA_Short'] = df['Adj Close'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['Adj Close'].rolling(window=long_window).mean()

    # Condition to enter a long position (golden cross in low vol)
    entry_signal = (df['SMA_Short'] > df['SMA_Long']) & df['LowVol']

    # Condition to exit a long position (death cross)
    exit_signal = df['SMA_Short'] < df['SMA_Long']

    df['Signal'] = 0
    df.loc[entry_signal, 'Signal'] = 1   # Go Long
    df.loc[exit_signal, 'Signal'] = 0    # Go Flat (Exit)

    # Use ffill to hold the position until an exit signal occurs
    df['Position'] = df['Signal'].ffill().fillna(0)

    # The final signal is the change in position
    # This is what you multiply by returns
    df['Signal'] = df['Position'].diff().fillna(0)

    return df