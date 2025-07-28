import pandas as pd

def backtest(data: pd.DataFrame, signal_column: str = 'Signal'):
    """
    Basic vectorized backtest on long-only or long/short strategy.
    Assumes signal values are -1, 0, or 1.
    Returns portfolio equity curve and performance metrics.
    """
    df = data.copy()
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df[signal_column] * df['Returns']
    df['Equity_Curve'] = (1 + df['Strategy_Returns']).cumprod()
    return df
