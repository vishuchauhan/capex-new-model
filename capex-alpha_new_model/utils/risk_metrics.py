import numpy as np

def calculate_metrics(returns):

    returns = returns.dropna()

    if len(returns) == 0 or returns.std() == 0:
        sharpe = 0
        volatility = 0
    else:
        sharpe = np.sqrt(252) * returns.mean() / returns.std()
        volatility = returns.std() * np.sqrt(252)

    cumulative = (1 + returns).cumprod()

    if len(cumulative) == 0:
        max_drawdown = 0
    else:
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        max_drawdown = drawdown.min()

    return {
        "Sharpe": sharpe,
        "Max Drawdown": max_drawdown,
        "Volatility": volatility
    }