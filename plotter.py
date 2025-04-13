import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FOREX_API_KEY")

async def plot_price_chart(pair: str) -> str:
    from_symbol = pair[:3]
    to_symbol = pair[3:]

    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval=60min&apikey={API_KEY}&outputsize=compact"
    res = requests.get(url).json()

    try:
        data = res["Time Series FX (60min)"]
        df = pd.DataFrame(data).T.astype(float).sort_index()

        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["4. close"], label="Close Price", color="blue")
        plt.title(f"{pair} - Harga Terakhir")
        plt.xlabel("Waktu")
        plt.ylabel("Harga")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.legend()

        filename = f"{pair}_chart.png"
        plt.savefig(filename)
        plt.close()

        return filename
    except:
        return None
