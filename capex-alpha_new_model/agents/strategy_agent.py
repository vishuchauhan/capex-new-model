def strategy_agent(financial_scores, industry_ratio):

    import pandas as pd

    strategy_scores = {}

    # Convert to Series for ranking
    s = pd.Series(financial_scores)

    # 🔥 RANK BASED (FIX)
    ranks = s.rank(pct=True)   # values between 0 and 1

    for ticker in financial_scores:

        normalized = ranks[ticker]

        # Convert to 1–3 scale
        strat_score = 1 + 2 * normalized

        # Industry boost
        if industry_ratio > 0.5:
            strat_score += 0.5

        strategy_scores[ticker] = strat_score

    return strategy_scores