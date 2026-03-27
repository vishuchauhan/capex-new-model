import pandas as pd
import os
from datetime import datetime

def save_to_excel(portfolio, benchmark, selections):

    os.makedirs("output", exist_ok=True)

    portfolio = portfolio.squeeze()
    benchmark = benchmark.squeeze()

    benchmark = benchmark.reindex(portfolio.index)

    # FIX WARNING
    portfolio_ret = portfolio.pct_change(fill_method=None)
    benchmark_ret = benchmark.pct_change(fill_method=None)

    alpha = portfolio_ret - benchmark_ret

    perf_df = pd.DataFrame({
        "Portfolio": portfolio,
        "NIFTY": benchmark,
        "Portfolio Return": portfolio_ret,
        "NIFTY Return": benchmark_ret,
        "Alpha": alpha
    })

    try:
        with pd.ExcelWriter("output/results.xlsx") as writer:
            perf_df.to_excel(writer, sheet_name="Performance")
            selections.to_excel(writer, sheet_name="Stock Picks")

        print("✅ Results saved to output/results.xlsx")

    except PermissionError:
        # 🔥 fallback: save new file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/results_{timestamp}.xlsx"

        with pd.ExcelWriter(filename) as writer:
            perf_df.to_excel(writer, sheet_name="Performance")
            selections.to_excel(writer, sheet_name="Stock Picks")

        print(f"⚠️ File open! Saved instead as {filename}")