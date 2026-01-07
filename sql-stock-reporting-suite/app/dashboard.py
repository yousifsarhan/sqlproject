import os
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError

    MYSQL_AVAILABLE = True
    MYSQL_IMPORT_ERROR = ""
except Exception as exc:  # pragma: no cover - runtime environment only
    mysql = None
    MySQLError = Exception
    MYSQL_AVAILABLE = False
    MYSQL_IMPORT_ERROR = str(exc)

load_dotenv()

def get_db_config() -> dict:
    # Prefer Streamlit Cloud secrets when available; fall back to local .env.
    if "DB_HOST" in st.secrets:
        return {
            "host": st.secrets["DB_HOST"],
            "user": st.secrets["DB_USER"],
            "password": st.secrets["DB_PASSWORD"],
            "database": st.secrets["DB_NAME"],
            "port": int(st.secrets.get("DB_PORT", 3306)),
        }

    return {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "port": int(os.getenv("DB_PORT", "3306")),
    }

st.title("SQL Stock Reporting Suite")
st.caption("Prices stored in MySQL, reported via Views/Procedures")

def render_demo() -> None:
    now = datetime.now()
    latest = pd.DataFrame(
        [
            {"symbol": "SPY", "name": "S&P 500 ETF", "price": 691.81, "fetched_at": now},
            {"symbol": "NVDA", "name": "NVIDIA", "price": 187.24, "fetched_at": now},
            {"symbol": "TSLA", "name": "Tesla", "price": 251.02, "fetched_at": now},
        ]
    )
    st.subheader("Latest Prices (demo)")
    st.dataframe(latest, use_container_width=True)

    st.subheader("Minute Aggregation (demo)")
    sym = st.selectbox("Symbol", ["SPY", "NVDA", "TSLA"])
    minutes = [now - timedelta(minutes=i) for i in range(120)][::-1]
    history = pd.DataFrame(
        {
            "minute_bucket": minutes,
            "avg_price": [latest.loc[latest["symbol"] == sym, "price"].iloc[0]] * 120,
        }
    )
    st.line_chart(history.set_index("minute_bucket"))


if not MYSQL_AVAILABLE:
    st.warning("MySQL connector not installed. Showing demo data.")
    st.caption(f"Details: {MYSQL_IMPORT_ERROR}")
    render_demo()
    st.stop()

try:
    conn = mysql.connector.connect(**get_db_config())
except MySQLError as exc:
    st.error("Database connection failed. Check DB_* secrets/env and remote host.")
    st.caption(f"Details: {exc}")
    render_demo()
    st.stop()

st.subheader("Latest Prices (vw_latest_price)")
latest = pd.read_sql("SELECT * FROM vw_latest_price ORDER BY symbol", conn)
st.dataframe(latest, use_container_width=True)

st.subheader("Minute Aggregation (vw_minute_prices)")
sym = st.selectbox("Symbol", ["SPY", "NVDA", "TSLA"])

history = pd.read_sql(
    f"""
    SELECT minute_bucket, avg_price
    FROM vw_minute_prices
    WHERE symbol = '{sym}'
    ORDER BY minute_bucket DESC
    LIMIT 120
    """,
    conn,
)
history = history.sort_values("minute_bucket")
st.line_chart(history.set_index("minute_bucket"))
