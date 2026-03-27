import pandas as pd

def load_capex_data():

    df = pd.read_excel("data/capex_data.xlsx")

    df = df.sort_values(["Ticker", "Year"])

    return df