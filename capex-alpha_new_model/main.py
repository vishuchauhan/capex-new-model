import pandas as pd
import matplotlib.pyplot as plt
import os

from data.capex_loader import load_capex_data
from data.market_data import load_market_data
from agents.financial_agent import financial_agent
from agents.nlp_agent import nlp_agent
from agents.industry_agent import industry_agent
from agents.strategy_agent import strategy_agent
from scoring.scoring_engine import compute_capex_scores
from backtest.capex_backtest import rolling_capex_backtest
from utils.risk_metrics import calculate_metrics
from utils.alpha_analysis import alpha_decomposition
from utils.advanced_metrics import advanced_metrics
from backtest.rolling_backtest import get_benchmark

# =========================
# LOAD DATA
# =========================

capex_df = load_capex_data()

tickers = (
    capex_df["Ticker"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

price_data = load_market_data(tickers, "2020-01-01", "2024-01-01")

# =========================
# NLP DATA
# =========================

news_dict = {
    ticker: [
        f"{ticker} announces expansion",
        f"{ticker} increases capex",
        f"{ticker} builds new plant"
    ]
    for ticker in tickers
}

nlp_scores = nlp_agent(news_dict)

# =========================
# SCORING FUNCTION
# =========================

def scoring_func(capex_df, year):

    fin_scores, fin_components = financial_agent(capex_df, year)
    industry_ratio = industry_agent(fin_scores)
    strat_scores = strategy_agent(fin_scores, industry_ratio)

    score_df = compute_capex_scores(fin_scores, strat_scores, nlp_scores)

    return score_df

# =========================
# BACKTEST
# =========================

portfolio_cum, portfolio_returns = rolling_capex_backtest(
    price_data,
    capex_df,
    scoring_func,
    top_n=5
)

# =========================
# BENCHMARK
# =========================

benchmark, _ = get_benchmark("2020-01-01", "2024-01-01")

portfolio_cum = portfolio_cum.squeeze()
benchmark = benchmark.squeeze()

# 🔥 FIX 1: Align + remove NaNs (clean Excel)
benchmark = benchmark.reindex(portfolio_cum.index)
portfolio_cum = portfolio_cum.fillna(0)
benchmark = benchmark.fillna(0)

# =========================
# METRICS
# =========================

metrics = calculate_metrics(portfolio_returns)

print("\n=== METRICS ===")
for k, v in metrics.items():
    print(k, round(v, 3))

# =========================
# FINAL SCORES
# =========================

latest_year = capex_df["Year"].max()
final_scores_df = scoring_func(capex_df, latest_year)
final_scores_df = final_scores_df.sort_values("Capex Score", ascending=False)

# 🔥 FIX 2: Clean score NaNs (better Excel output)
final_scores_df = final_scores_df.fillna(0)

# =========================
# ALPHA DECOMPOSITION
# =========================

alpha_df = alpha_decomposition(final_scores_df)

# =========================
# TOP PICKS
# =========================

top_picks = final_scores_df.head(5).copy()

def explain(row):
    reasons = []

    if row["Financial Score"] > 0:
        reasons.append("Strong capex growth")

    if row["Strategy Score"] >= 2:
        reasons.append("Industry leader")

    if row["NLP Score"] > 0:
        reasons.append("Expansion narrative")

    return " | ".join(reasons)

top_picks["Reason"] = top_picks.apply(explain, axis=1)
top_picks["Recommendation"] = "BUY"

# =========================
# ADVANCED METRICS
# =========================

rolling_sharpe, drawdown_series = advanced_metrics(portfolio_returns)

# 🔥 FIX 3: Rename series (removes "0" column issue in Excel)
rolling_sharpe = rolling_sharpe.rename("Rolling Sharpe")
drawdown_series = drawdown_series.rename("Drawdown")

# 🔥 FIX 4: Clean NaNs
rolling_sharpe = rolling_sharpe.fillna(0)
drawdown_series = drawdown_series.fillna(0)

# =========================
# SAVE EXCEL
# =========================

os.makedirs("output", exist_ok=True)

with pd.ExcelWriter("output/final_capex_results.xlsx") as writer:

    pd.DataFrame({
        "Portfolio": portfolio_cum,
        "NIFTY": benchmark
    }).to_excel(writer, sheet_name="Performance")

    final_scores_df.to_excel(writer, sheet_name="Capex Scores")
    top_picks.to_excel(writer, sheet_name="Top Picks")
    alpha_df.to_excel(writer, sheet_name="Alpha Breakdown")

    final_scores_df[
        ["Financial Contribution", "Strategy Contribution", "NLP Contribution"]
    ].to_excel(writer, sheet_name="Score Contributions")

    rolling_sharpe.to_excel(writer, sheet_name="Rolling Sharpe")
    drawdown_series.to_excel(writer, sheet_name="Drawdown Curve")

print("✅ ALL OUTPUTS SAVED")

# =========================
# PLOTS
# =========================

plt.figure(figsize=(10, 5))
plt.plot(portfolio_cum, label="Capex Strategy")
plt.plot(benchmark, label="NIFTY")
plt.legend()
plt.title("Dynamic Capex Strategy vs NIFTY")
plt.show()

plt.figure()
plt.plot(drawdown_series)
plt.title("Drawdown Curve")
plt.show()

plt.figure()
plt.plot(rolling_sharpe)
plt.title("Rolling Sharpe Ratio")
plt.show()