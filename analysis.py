import requests
import os
import pandas as pd
import ta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FOREX_API_KEY")

async def get_analysis(pair: str) -> str:
    from_symbol = pair[:3]
    to_symbol = pair[3:]

    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval=60min&apikey={API_KEY}&outputsize=compact"
    res = requests.get(url).json()

    try:
        data = res["Time Series FX (60min)"]
        df = pd.DataFrame(data).T.astype(float).sort_index()

        df["rsi"] = ta.momentum.RSIIndicator(close=df["4. close"]).rsi()
        df["macd"] = ta.trend.MACD(close=df["4. close"]).macd_diff()
        df["sma"] = ta.trend.SMAIndicator(close=df["4. close"], window=14).sma_indicator()

        rsi = df["rsi"].iloc[-1]
        macd = df["macd"].iloc[-1]
        sma = df["sma"].iloc[-1]
        last_close = df["4. close"].iloc[-1]

        signal = "BUY" if macd > 0 and rsi < 70 else "SELL" if macd < 0 and rsi > 30 else "HOLD"

        return (
            f"Analisa {pair}:\n"
            f"Harga terakhir: {last_close:.4f}\n"
            f"RSI: {rsi:.2f}\n"
            f"MACD: {macd:.4f}\n"
            f"SMA (14): {sma:.4f}\n"
            f"Sinyal: {signal}"
        )
    except Exception as e:
        return "Gagal mengambil analisa teknikal."
