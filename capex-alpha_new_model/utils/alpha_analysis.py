import pandas as pd

def alpha_decomposition(score_df):

    total = score_df["Capex Score"].sum()

    if total == 0:
        return pd.DataFrame({
            "Component": ["Financial", "Strategy", "NLP"],
            "Contribution %": [0, 0, 0]
        })

    financial_alpha = score_df["Financial Contribution"].sum() / total
    strategy_alpha = score_df["Strategy Contribution"].sum() / total
    nlp_alpha = score_df["NLP Contribution"].sum() / total

    return pd.DataFrame({
        "Component": ["Financial", "Strategy", "NLP"],
        "Contribution %": [
            financial_alpha,
            strategy_alpha,
            nlp_alpha
        ]
    })