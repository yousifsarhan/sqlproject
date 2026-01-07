import os
import pandas as pd
import mysql.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_db_config() -> dict:
    # Prefer Streamlit Cloud secrets when available; fall back to local .env.
    if "DB_HOST" in st.secrets:
        return {
            "host": st.secrets["DB_HOST"],
            "user": st.secrets["DB_USER"],
            "password": st.secrets["DB_PASSWORD"],
            "database": st.secrets["DB_NAME"],
        }

    return {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
    }

st.title("SQL Stock Reporting Suite")
st.caption("Prices stored in MySQL, reported via Views/Procedures")

try:
    conn = mysql.connector.connect(**get_db_config())
except mysql.connector.Error as exc:
    st.error(f"Database connection failed: {exc}")
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
