import streamlit as st
import duckdb
import pandas as pd
import altair as alt

# --- Connect to DuckDB database ---
conn = duckdb.connect(
    r"C:\kev\Ethereum_Blockchain\eth_blockchain\ethereum_dbt\dev.duckdb"
)
st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("📊 Crypto Daily Metrics Dashboard")

# --- Sidebar filters ---
assets = conn.execute("SELECT DISTINCT asset FROM main.fct_crypto_daily").fetchall()
assets = [a[0] for a in assets]

selected_assets = st.sidebar.multiselect(
    "Select Assets", options=assets, default=assets[:5]
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=[pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31")]
)

# --- Query filtered data ---
query = f"""
SELECT *
FROM main.fct_crypto_daily
WHERE asset IN ({','.join([f"'{a}'" for a in selected_assets])})
  AND date BETWEEN '{date_range[0]}' AND '{date_range[1]}'
ORDER BY date
"""

df = conn.execute(query).fetchdf()

# --- Metrics ---
st.subheader("Summary Metrics")
st.metric("Total Records", len(df))
st.metric("Average Daily Return", round(df['daily_return'].mean(), 4))

# --- Charts ---
st.subheader("Daily Return Over Time")
chart = alt.Chart(df).mark_line().encode(
    x='date:T',
    y='daily_return:Q',
    color='asset:N'
).interactive()

st.altair_chart(chart, use_container_width=True)

st.subheader("Volume Over Time")
volume_chart = alt.Chart(df).mark_bar().encode(
    x='date:T',
    y='volume:Q',
    color='asset:N'
).interactive()

st.altair_chart(volume_chart, use_container_width=True)
