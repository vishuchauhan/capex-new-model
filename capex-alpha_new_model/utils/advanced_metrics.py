import pandas as pd
import numpy as np

def advanced_metrics(returns):

    rolling_sharpe = returns.rolling(60).mean() / returns.rolling(60).std()

    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak

    return rolling_sharpe, drawdown