# app.py
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# ------------------------------
# 1️⃣ Connect to DuckDB
# ------------------------------
DB_PATH = r"C:\kev\Ethereum_Blockchain\eth_blockchain\ethereum_dbt\dev.duckdb"
conn = duckdb.connect(DB_PATH, read_only=True)

# ------------------------------
# 2️⃣ Sidebar Controls
# ------------------------------
st.sidebar.header("Select Assets & Date Range")

# Get distinct assets from the table
assets_df = conn.execute("SELECT DISTINCT asset FROM int_crypto_features ORDER BY asset").df()
all_assets = assets_df['asset'].tolist()

selected_assets = st.sidebar.multiselect("Select Assets", all_assets, default=all_assets[:5])

# Get min and max dates
min_date, max_date = conn.execute("SELECT MIN(date), MAX(date) FROM int_crypto_features").fetchone()

# Date range picker safely handles single or multiple selections
selected_dates = st.sidebar.date_input(
    "Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Ensure we always have start_date and end_date
if isinstance(selected_dates, (tuple, list)):
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

# ------------------------------
# 3️⃣ Query the filtered data
# ------------------------------
query = f"""
SELECT date, asset, close_price, daily_return, volume
FROM int_crypto_features
WHERE asset IN ({','.join([f"'{a}'" for a in selected_assets])})
  AND date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY asset, date
"""
df = conn.execute(query).df()

# ------------------------------
# 4️⃣ Fix Column Names
# ------------------------------
df.columns = [c.lower() for c in df.columns]
df['date'] = pd.to_datetime(df['date'])

# ------------------------------
# 5️⃣ Dashboard Title & Summary
# ------------------------------
st.title("📊 Crypto Daily Metrics Dashboard")

st.subheader("Summary Metrics")
st.write("Total Records:", len(df))
st.write("Average Daily Return:", round(df['daily_return'].mean(), 6))

# ------------------------------
# 6️⃣ Daily Return Plot
# ------------------------------
st.subheader("Daily Return Over Time")
fig_return = px.line(
    df,
    x="date",
    y="daily_return",
    color="asset",
    labels={"daily_return": "Daily Return", "date": "Date"},
    title="Daily Return Trends"
)
st.plotly_chart(fig_return, width="stretch")

# ------------------------------
# 7️⃣ Volume Plot
# ------------------------------
st.subheader("Volume Over Time")
fig_volume = px.line(
    df,
    x="date",
    y="volume",
    color="asset",
    labels={"volume": "Volume", "date": "Date"},
    title="Trading Volume Trends"
)
st.plotly_chart(fig_volume, width="stretch")
