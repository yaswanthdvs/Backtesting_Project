import numpy as np
import pandas as pd

def sharpe_ratio(returns, risk_free_rate=0.0):
    excess_returns = returns - risk_free_rate
    return np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)

def max_drawdown(equity_curve):
    roll_max = equity_curve.cummax()
    drawdown = (equity_curve - roll_max) / roll_max
    return drawdown.min()

def sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    excess_returns = returns - risk_free_rate
    negative_returns = excess_returns[excess_returns < 0]
    downside_std = negative_returns.std()
    if downside_std == 0:
        return np.nan
    return np.sqrt(252) * excess_returns.mean() / downside_std

def calmar_ratio(returns: pd.Series, equity_curve: pd.Series) -> float:
    cumulative_return = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1
    drawdown = abs(max_drawdown(equity_curve))
    return cumulative_return / drawdown if drawdown != 0 else np.nan

import pandas as pd

def trade_statistics(signals: pd.Series, returns: pd.Series) -> dict:
    """
    Compute detailed trade-level statistics from signals and returns.
    Assumes:
        - signals ∈ {-1, 0, 1}
        - trades are executed on the next bar
    """
    signals = signals.shift(1).fillna(0)  # Apply signal with 1-bar lag
    positions = signals.replace(0, method='ffill').fillna(0)
    strategy_returns = positions * returns

    # Identify trade start/end
    position_change = positions != positions.shift(1)
    trade_id = position_change.cumsum()
    strategy_returns = strategy_returns[positions != 0]
    durations = positions[positions != 0].groupby(trade_id).size()

    # Group returns by trade ID
    trade_returns = strategy_returns.groupby(trade_id).sum()

    num_trades = len(trade_returns)
    wins = trade_returns[trade_returns > 0]
    losses = trade_returns[trade_returns < 0]

    stats = {
        "Number of Trades": num_trades,
        "Win Rate": len(wins) / num_trades if num_trades else 0,
        "Average Win": wins.mean() if not wins.empty else 0,
        "Median Win": wins.median() if not wins.empty else 0,
        "Average Loss": losses.mean() if not losses.empty else 0,
        "Median Loss": losses.median() if not losses.empty else 0,
        "Win/Loss Ratio": (wins.mean() / abs(losses.mean())) if (not wins.empty and not losses.empty) else 0,
        "Average Holding Period": durations.mean() if not durations.empty else 0
    }

    return stats

