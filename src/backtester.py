import pandas as pd

def backtest(data: pd.DataFrame, signal_column: str = 'Signal', cost: float = 0.0005):
    """
    Vectorized backtest engine for long-only or long/short strategies.

    Parameters:
    - data: pd.DataFrame with 'Close' prices and a signal column
    - signal_column: name of the column with trading signals (-1, 0, 1)
    - cost: transaction cost per trade (e.g., 0.0005 for 5 bps)

    Returns:
    - DataFrame with strategy returns, benchmark returns, and equity curve
    """
    df = data.copy()
    df['Returns'] = df['Close'].pct_change()
    
    # Shift signal to avoid lookahead bias
    df['Signal'] = df[signal_column].shift(1)

    # Compute trade cost when signal changes
    df['Trade'] = df['Signal'].diff().abs().fillna(0)
    
    # Apply strategy returns with transaction costs
    df['Strategy_Returns'] = df['Signal'] * df['Returns']
    df['Strategy_Returns'] -= df['Trade'] * cost

    # Compute equity curves
    df['Equity_Curve'] = (1 + df['Strategy_Returns']).cumprod()
    df['Benchmark'] = (1 + df['Returns'].fillna(0)).cumprod()

    return df