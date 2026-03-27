import requests

def get_news(company, api_key):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"
    response = requests.get(url).json()

    headlines = [article["title"] for article in response["articles"][:10]]
    return headlines