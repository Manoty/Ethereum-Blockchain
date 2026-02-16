# app.py
import os
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ------------------------------
# 1️⃣ Connect to DuckDB
# ------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "dev.duckdb")
conn = duckdb.connect(DB_PATH, read_only=True)

# ------------------------------
# 2️⃣ Sidebar Controls
# ------------------------------
st.sidebar.header("Select Assets & Date Range")

# Get distinct assets from the table
assets_df = conn.execute("SELECT DISTINCT asset FROM int_crypto_features ORDER BY asset").df()
all_assets = assets_df['asset'].tolist()

selected_assets = st.sidebar.multiselect("Select Assets", all_assets, default=all_assets[:5])

# Get min and max dates from the DB
min_date_raw, max_date_raw = conn.execute("SELECT MIN(date), MAX(date) FROM int_crypto_features").fetchone()
min_date = pd.to_datetime(min_date_raw).date()
max_date = pd.to_datetime(max_date_raw).date()

# Default to last 30 days
default_start = max(min_date, max_date - pd.Timedelta(days=30))
default_end = max_date

# Date picker with proper min/max and defaults
selected_dates = st.sidebar.date_input(
    "Date Range",
    value=[default_start, default_end],
    min_value=min_date,
    max_value=max_date
)

# Ensure two dates
if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

# Convert to string format for DuckDB
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# ------------------------------
# 3️⃣ Query the filtered data
# ------------------------------
query = f"""
SELECT date, asset, close_price, open_price, high, low, volume, daily_return, log_return
FROM int_crypto_features
WHERE asset IN ({','.join([f"'{a}'" for a in selected_assets])})
  AND date BETWEEN '{start_date_str}' AND '{end_date_str}'
ORDER BY asset, date
"""
df = conn.execute(query).df()

# ------------------------------
# 4️⃣ Fix Column Names
# ------------------------------
df.columns = [c.lower() for c in df.columns]
df['date'] = pd.to_datetime(df['date'])

# ------------------------------
# 5️⃣ Calculate 7-Day Moving Average
# ------------------------------
df = df.sort_values(['asset', 'date'])
df['daily_return_7d_ma'] = df.groupby('asset')['daily_return'].transform(lambda x: x.rolling(7, min_periods=1).mean())

# ------------------------------
# 6️⃣ Dashboard Title & Summary
# ------------------------------
st.title("📊 Crypto Daily Metrics Dashboard")
st.write("Analyze daily returns, volume, and risk metrics for your selected crypto assets.")
st.subheader("Summary Metrics")
st.write("Total Records:", len(df))
st.write("Average Daily Return:", round(df['daily_return'].mean(), 6))

# ------------------------------
# 7️⃣ Daily Return Plot
# ------------------------------
st.subheader("Daily Return Over Time")
st.write("Shows daily return trends for selected assets.")
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
# 8️⃣ 7-Day Moving Average Plot
# ------------------------------
st.subheader("7-Day Moving Average of Daily Return")
st.write("Smooths daily returns to show short-term trends.")
fig_ma = px.line(
    df,
    x="date",
    y="daily_return_7d_ma",
    color="asset",
    labels={"daily_return_7d_ma": "7-Day MA Daily Return", "date": "Date"},
    title="Smoothed Daily Return Trends"
)
st.plotly_chart(fig_ma, width="stretch")

# ------------------------------
# 9️⃣ Log Return Plot
# ------------------------------
st.subheader("Log Return Over Time")
st.write("Shows logarithmic returns, useful for compounding insights.")
fig_log = px.line(
    df,
    x="date",
    y="log_return",
    color="asset",
    labels={"log_return": "Log Return", "date": "Date"},
    title="Log Return Trends"
)
st.plotly_chart(fig_log, width="stretch")

# ------------------------------
# 🔟 Volume Plot
# ------------------------------
st.subheader("Volume Over Time")
st.write("Daily traded volume trends.")
fig_volume = px.line(
    df,
    x="date",
    y="volume",
    color="asset",
    labels={"volume": "Volume", "date": "Date"},
    title="Trading Volume Trends"
)
st.plotly_chart(fig_volume, width="stretch")

# ------------------------------
# 1️⃣1️⃣ Multi-Metric Toggle Plot with Dual Y-Axis
# ------------------------------
st.subheader("Interactive Multi-Metric Plot (Dual Y-Axis)")
st.write("Select multiple metrics and view returns vs volume on dual axes.")
metrics = st.multiselect(
    "Select Metrics to Display",
    options=["daily_return", "daily_return_7d_ma", "log_return", "volume"],
    default=["daily_return", "daily_return_7d_ma"]
)
if metrics:
    use_secondary_y = "volume" in metrics
    fig_multi = make_subplots(specs=[[{"secondary_y": use_secondary_y}]])
    for metric in metrics:
        for asset in df['asset'].unique():
            df_asset = df[df['asset'] == asset]
            if metric == "volume":
                fig_multi.add_trace(
                    go.Scatter(
                        x=df_asset['date'],
                        y=df_asset[metric],
                        mode='lines',
                        name=f"{asset} - {metric}"
                    ),
                    secondary_y=True
                )
            else:
                fig_multi.add_trace(
                    go.Scatter(
                        x=df_asset['date'],
                        y=df_asset[metric],
                        mode='lines',
                        name=f"{asset} - {metric}"
                    ),
                    secondary_y=False
                )
    fig_multi.update_layout(title_text="Selected Metrics Over Time (Dual Y-Axis)", xaxis_title="Date")
    if use_secondary_y:
        fig_multi.update_yaxes(title_text="Returns", secondary_y=False)
        fig_multi.update_yaxes(title_text="Volume", secondary_y=True)
    else:
        fig_multi.update_yaxes(title_text="Returns")
    st.plotly_chart(fig_multi, width="stretch")
else:
    st.info("Select at least one metric to display.")

# ------------------------------
# 1️⃣2️⃣ Rolling Sharpe Ratio
# ------------------------------
st.subheader("Rolling 7-Day Sharpe Ratio")
st.write("Risk-adjusted performance: average return / volatility over a rolling window.")
rolling_window = 7
df_sharpe = df.copy()
df_sharpe['sharpe_7d'] = df_sharpe.groupby('asset')['daily_return'].transform(
    lambda x: x.rolling(rolling_window).mean() / x.rolling(rolling_window).std()
)
fig_sharpe = px.line(
    df_sharpe,
    x='date',
    y='sharpe_7d',
    color='asset',
    labels={'sharpe_7d': 'Rolling Sharpe Ratio', 'date': 'Date'},
    title='Rolling 7-Day Sharpe Ratio'
)
st.plotly_chart(fig_sharpe, width="stretch")

# ------------------------------
# 1️⃣3️⃣ Correlation Matrix Heatmap
# ------------------------------
st.subheader("Correlation Matrix Between Selected Assets")
st.write("Shows how selected assets move together (1 = perfect correlation, -1 = inverse).")
pivot_returns = df.pivot(index='date', columns='asset', values='daily_return')
corr_matrix = pivot_returns.corr()
fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    zmin=-1,
    zmax=1,
    labels={'color': 'Correlation'}
)
st.plotly_chart(fig_corr, width="stretch")

# ------------------------------
# 1️⃣4️⃣ Cumulative Return Plot
# ------------------------------
st.subheader("Cumulative Return Over Time")
st.write("Shows total compounded return for each asset over the selected date range.")
df_cum = df.copy()
df_cum['cum_return'] = df_cum.groupby('asset')['daily_return'].apply(lambda x: (1 + x).cumprod() - 1)
fig_cum = px.line(
    df_cum,
    x='date',
    y='cum_return',
    color='asset',
    labels={'cum_return': 'Cumulative Return', 'date': 'Date'},
    title='Cumulative Return Trends'
)
st.plotly_chart(fig_cum, width="stretch")
