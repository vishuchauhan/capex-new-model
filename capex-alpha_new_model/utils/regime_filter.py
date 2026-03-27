import pandas as pd

def regime_filter(price_data):

    returns = price_data.pct_change()

    market_return = returns.mean(axis=1)

    rolling_mean = market_return.rolling(50).mean()

    regime = rolling_mean > 0  # True = bullish

    return regime