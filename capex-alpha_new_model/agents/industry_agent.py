def industry_agent(financial_scores):

    values = list(financial_scores.values())

    if len(values) == 0:
        return 0.5

    # % of companies with positive capex signal
    positive = sum(1 for v in values if v > 0)

    ratio = positive / len(values)

    return ratio