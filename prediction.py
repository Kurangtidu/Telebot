import requests
import os
import pandas as pd
from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression
import numpy as np

load_dotenv()
API_KEY = os.getenv("FOREX_API_KEY")

async def predict_price(pair: str) -> str:
    from_symbol = pair[:3]
    to_symbol = pair[3:]

    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval=60min&apikey={API_KEY}&outputsize=compact"
    res = requests.get(url).json()

    try:
        data = res["Time Series FX (60min)"]
        df = pd.DataFrame(data).T.astype(float).sort_index()
        df["target"] = df["4. close"].shift(-1)
        df.dropna(inplace=True)

        X = df[["4. close"]].values
        y = df["target"].values

        model = LinearRegression()
        model.fit(X, y)

        last_price = df["4. close"].iloc[-1]
        pred_price = model.predict([[last_price]])[0]

        direction = "naik" if pred_price > last_price else "turun" if pred_price < last_price else "stabil"
        return (
            f"Prediksi {pair}:\n"
            f"Harga saat ini: {last_price:.4f}\n"
            f"Prediksi harga berikutnya: {pred_price:.4f}\n"
            f"Prediksi arah: {direction.upper()}"
        )
    except Exception as e:
        return "Gagal melakukan prediksi. Coba beberapa saat lagi."
