def financial_agent(capex_df, current_year):

    scores = {}
    components = {}

    grouped = capex_df.groupby("Ticker")

    for ticker, data in grouped:

        data = data.sort_values("Year")
        data = data[data["Year"] <= current_year]

        if len(data) < 2:
            scores[ticker] = 0
            components[ticker] = {
                "cwip_growth": 0,
                "cwip_acceleration": 0,
                "asset_growth": 0,
                "debt_growth": 0
            }
            continue

        # =========================
        # CAPEX SIGNALS
        # =========================

        cwip_series = data["CWIP"].pct_change()

        cwip_growth = cwip_series.iloc[-1]
        cwip_acceleration = cwip_series.diff().iloc[-1]

        asset_growth = data["TotalAssets"].pct_change().iloc[-1]
        debt_growth = data["Debt"].pct_change().iloc[-1]

        # =========================
        # CONTINUOUS SCORING
        # =========================

        score = (
            4 * cwip_growth +
            3 * cwip_acceleration +
            2 * asset_growth +
            1 * debt_growth
        )

        scores[ticker] = score

        components[ticker] = {
            "cwip_growth": cwip_growth,
            "cwip_acceleration": cwip_acceleration,
            "asset_growth": asset_growth,
            "debt_growth": debt_growth
        }

    return scores, components