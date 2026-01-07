import os, time
import requests
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
DB = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

SYMBOLS = ["SPY", "NVDA", "TSLA"]


def get_price(symbol: str) -> float | None:
    url = "https://www.alphavantage.co/query"
    params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": API_KEY}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    q = data.get("Global Quote", {})
    price_str = q.get("05. price")
    return float(price_str) if price_str else None

def main():
    conn = mysql.connector.connect(**DB)
    cur = conn.cursor()

    # map symbol -> id
    cur.execute("SELECT id, symbol FROM symbols")
    symbol_map = {sym: sid for sid, sym in cur.fetchall()}

    while True:
        for sym in SYMBOLS:
            price = get_price(sym)
            if price is not None:
                sid = symbol_map[sym]
                now = datetime.now()
                cur.execute(
                    "INSERT INTO price_ticks(symbol_id, price, fetched_at, source) VALUES (%s,%s,%s,%s)",
                    (sid, price, now, "alphavantage"),
                )
                conn.commit()
                print(f"[{now}] {sym} = {price}")
            else:
                print(f"⚠️ No price for {sym} (API limit or response)")
            time.sleep(15)  # small pause between symbols

        # IMPORTANT: Alpha Vantage free tier is very limited (25/day).
        # To avoid burning requests, sleep longer.
        time.sleep(60 * 10)  # every 10 minutes

if __name__ == "__main__":
    main()
