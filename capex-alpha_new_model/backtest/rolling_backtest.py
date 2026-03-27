import pandas as pd
import numpy as np
import yfinance as yf

def rolling_backtest(price_data, scoring_func, top_n=3):

    returns = price_data.pct_change().dropna()
    dates = returns.resample("ME").first().index

    portfolio_returns = []
    selection_log = []

    for i in range(len(dates)-1):

        start = dates[i]
        end = dates[i+1]

        window = price_data.loc[:start]

        # 🔥 GET FULL DATA (not just scores)
        score_df = scoring_func(window)

        # Rank
        ranked = score_df.sort_values("final_score", ascending=False)

        selected = ranked.head(top_n)

        # Save selections
        for ticker, row in selected.iterrows():
            selection_log.append({
                "Date": start,
                "Stock": ticker,
                "Final Score": row["final_score"],
                "Financial Score": row["financial_score"],
                "Strategy Score": row["strategy_score"]
            })

        # Portfolio returns
        period_returns = returns.loc[start:end][selected.index].mean(axis=1)
        portfolio_returns.append(period_returns)

    portfolio_returns = pd.concat(portfolio_returns)
    cumulative = (1 + portfolio_returns).cumprod()

    selection_df = pd.DataFrame(selection_log)

    return cumulative, portfolio_returns, selection_df

def get_benchmark(start, end):

    data = yf.download("^NSEI", start=start, end=end)

    if "Adj Close" in data.columns:
        price = data["Adj Close"]
    else:
        price = data["Close"]

    returns = price.pct_change().dropna()
    cumulative = (1 + returns).cumprod()

    return cumulative, returns


def sharpe_ratio(returns):
    return np.sqrt(252) * returns.mean() / returns.std()