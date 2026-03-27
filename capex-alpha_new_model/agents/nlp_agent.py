def nlp_agent(news_dict):

    keywords = ["expansion", "capacity", "plant", "investment", "capex"]

    scores = {}

    for ticker, headlines in news_dict.items():

        score = 0

        for text in headlines:
            text = text.lower()

            for word in keywords:
                if word in text:
                    score += 1

        # Normalize score
        scores[ticker] = score / max(len(headlines), 1)

    return scores