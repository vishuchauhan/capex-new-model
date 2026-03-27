import pandas as pd
import numpy as np

def compute_capex_scores(fin_scores, strat_scores, nlp_scores):

    records = []

    for ticker in fin_scores:

        # =========================
        # SAFE FETCH
        # =========================
        fin = fin_scores.get(ticker, 0)
        strat = strat_scores.get(ticker, 0)
        nlp = nlp_scores.get(ticker, 0)

        # 🔥 FIX 1: Handle NaNs
        fin = 0 if pd.isna(fin) else fin
        strat = 0 if pd.isna(strat) else strat
        nlp = 0 if pd.isna(nlp) else nlp

        # 🔥 FIX 2: Normalize extreme financial values (prevents cancellation)
        # scale to manageable range
        fin_scaled = np.tanh(fin / 5)   # keeps values between -1 and 1

        # 🔥 FIX 3: Ensure strategy is not zero baseline
        if strat == 0:
            strat = 1   # minimum participation (important)

        # =========================
        # FINAL SCORE
        # =========================
        final_score = (
            0.6 * fin_scaled +
            0.3 * strat +
            0.1 * nlp
        )

        # 🔥 FIX 4: Avoid exact zero (numerical stability)
        if final_score == 0:
            final_score = 1e-6

        records.append({
            "Ticker": ticker,

            # SCORES
            "Financial Score": fin,
            "Strategy Score": strat,
            "NLP Score": nlp,
            "Capex Score": final_score,

            # CONTRIBUTIONS (based on scaled values)
            "Financial Contribution": 0.6 * fin_scaled,
            "Strategy Contribution": 0.3 * strat,
            "NLP Contribution": 0.1 * nlp
        })

    df = pd.DataFrame(records)

    # 🔥 FIX 5: Ensure no missing tickers / proper index
    df = df.dropna(subset=["Ticker"])
    df = df.set_index("Ticker")

    return df