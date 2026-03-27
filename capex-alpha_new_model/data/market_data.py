import yfinance as yf

def load_market_data(tickers, start, end):

    data = yf.download(tickers, start=start, end=end)

    if "Adj Close" in data.columns:
        price = data["Adj Close"]
    else:
        price = data["Close"]

    return price