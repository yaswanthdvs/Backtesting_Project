import pandas as pd

def analyze_trades(df: pd.DataFrame, signal_col: str = 'Signal', return_col: str = 'Returns'):
    """
    Extract detailed trade-level diagnostics from signal and return series.
    Assumes 'Signal' is +1 for entry, -1 for exit.
    """
    df = df.copy()
    df['Signal'] = df[signal_col]
    df['Returns'] = df[return_col]
    
    trades = []
    in_trade = False
    entry_idx = None
    entry_date = None
    entry_price = None
    cum_return = 0

    for i in range(1, len(df)):
        row = df.iloc[i]
        date = df.index[i]

        # Entry
        if row['Signal'] == 1 and not in_trade:
            in_trade = True
            entry_idx = i
            entry_date = date
            cum_return = 0
            continue
        
        # Exit
        if row['Signal'] == -1 and in_trade:
            exit_idx = i
            exit_date = date
            period = df.iloc[entry_idx:exit_idx+1]
            cum_return = (1 + period['Returns']).prod() - 1
            duration = exit_idx - entry_idx

            trades.append({
                "Entry Date": entry_date,
                "Exit Date": exit_date,
                "Return": cum_return,
                "Duration (days)": duration,
                "Win": cum_return > 0
            })

            in_trade = False

    return pd.DataFrame(trades)
