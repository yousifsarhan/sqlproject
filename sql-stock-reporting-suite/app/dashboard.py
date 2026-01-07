import os
import pandas as pd
import mysql.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DB = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

st.title("SQL Stock Reporting Suite")
st.caption("Prices stored in MySQL, reported via Views/Procedures")

conn = mysql.connector.connect(**DB)

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
