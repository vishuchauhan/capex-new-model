import pandas as pd
from utils.regime_filter import regime_filter

def rolling_capex_backtest(price_data, capex_df, scoring_func, top_n=5):

    # =========================
    # PREPARE RETURNS
    # =========================
    returns = price_data.pct_change().dropna()

    # Monthly rebalance dates
    dates = returns.resample("ME").first().index

    # Regime detection
    regime = regime_filter(price_data)

    portfolio_returns = []

    # =========================
    # MAIN LOOP
    # =========================
    for date in dates[:-1]:

        current_year = date.year

        # Get scores
        score_df = scoring_func(capex_df, current_year)

        if score_df.empty:
            continue

        # Select top stocks
        selected = score_df.sort_values("Capex Score", ascending=False).head(top_n)

        if selected.empty:
            continue

        # =========================
        # SAFE WEIGHTS
        # =========================
        scores = selected["Capex Score"].copy()

        # 🔥 FIX 1: Replace NaN with mean (better than 0)
        scores = scores.fillna(scores.mean())

        # 🔥 FIX 2: Prevent division issues
        if scores.sum() == 0 or scores.isna().all():
            weights = pd.Series(1 / len(scores), index=scores.index)
        else:
            weights = scores / scores.sum()

        # =========================
        # NEXT PERIOD RETURNS
        # =========================
        next_period = returns.loc[date:date + pd.DateOffset(months=1)]

        if next_period.empty:
            continue

        # 🔥 FIX 3: Fill missing stock data (removes Excel blanks)
        period_data = next_period[selected.index].fillna(0)

        # Compute weighted returns
        period_returns = period_data.mul(weights, axis=1).sum(axis=1)

        # =========================
        # REGIME FILTER (SOFT)
        # =========================
        if date in regime.index and not regime.loc[date]:
            # reduce exposure, not kill it
            period_returns = period_returns * 0.7

        portfolio_returns.append(period_returns)

    # =========================
    # FINAL OUTPUT
    # =========================
    if len(portfolio_returns) == 0:
        return pd.Series(dtype=float), pd.Series(dtype=float)

    portfolio_returns = pd.concat(portfolio_returns)

    # 🔥 FIX 4: Drop any accidental NaNs
    portfolio_returns = portfolio_returns.fillna(0)

    cumulative = (1 + portfolio_returns).cumprod()

    return cumulative, portfolio_returns