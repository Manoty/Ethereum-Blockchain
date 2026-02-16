# app.py
import streamlit as st
import duckdb
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ==========================================================
# 1️⃣ Connect to DuckDB
# ==========================================================

DB_PATH = os.path.join(os.path.dirname(__file__), "dev.duckdb")
conn = duckdb.connect(DB_PATH, read_only=True)

# ==========================================================
# 2️⃣ Cached Data Loader
# ==========================================================

@st.cache_data
def load_data(query):
    return conn.execute(query).df()

# ==========================================================
# 3️⃣ Sidebar Controls
# ==========================================================

st.sidebar.header("Select Assets & Date Range")

assets_df = conn.execute(
    "SELECT DISTINCT asset FROM int_crypto_features ORDER BY asset"
).df()

all_assets = assets_df["asset"].tolist()

selected_assets = st.sidebar.multiselect(
    "Select Assets",
    all_assets,
    default=all_assets[:5]
)

if not selected_assets:
    st.warning("Please select at least one asset.")
    st.stop()

min_date_raw, max_date_raw = conn.execute(
    "SELECT MIN(date), MAX(date) FROM int_crypto_features"
).fetchone()

min_date = pd.to_datetime(min_date_raw).date()
max_date = pd.to_datetime(max_date_raw).date()

default_start = max(min_date, max_date - pd.Timedelta(days=30))
default_end = max_date

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=[default_start, default_end],
    min_value=min_date,
    max_value=max_date
)

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# ==========================================================
# 4️⃣ Query Filtered Data
# ==========================================================

query = f"""
SELECT date, asset, close_price, open_price, high, low,
       volume, daily_return, log_return
FROM int_crypto_features
WHERE asset IN ({','.join([f"'{a}'" for a in selected_assets])})
  AND date BETWEEN '{start_date_str}' AND '{end_date_str}'
ORDER BY asset, date
"""

df = load_data(query)

# ==========================================================
# 5️⃣ Data Cleaning
# ==========================================================

df.columns = [c.lower() for c in df.columns]
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["asset", "date"])

# ==========================================================
# 6️⃣ Feature Engineering
# ==========================================================

df["daily_return_7d_ma"] = (
    df.groupby("asset")["daily_return"]
    .transform(lambda x: x.rolling(7, min_periods=1).mean())
)

df["cumulative_return"] = (
    df.groupby("asset")["daily_return"]
    .transform(lambda x: (1 + x).cumprod())
)

df["volatility_30d"] = (
    df.groupby("asset")["daily_return"]
    .transform(lambda x: x.rolling(30, min_periods=5).std() * np.sqrt(365))
)

df["rolling_mean_30d"] = (
    df.groupby("asset")["daily_return"]
    .transform(lambda x: x.rolling(30, min_periods=5).mean())
)

df["rolling_sharpe_30d"] = (
    df["rolling_mean_30d"] /
    (df["volatility_30d"] / np.sqrt(365))
)

# ==========================================================
# 7️⃣ Dashboard Title
# ==========================================================

st.title("📊 Crypto Performance & Risk Analytics Dashboard")

st.markdown("""
## Executive Overview

This dashboard provides multi-asset crypto performance and portfolio risk analytics.

Capabilities include:
- Daily & log returns
- Rolling volatility & Sharpe ratio
- Cumulative growth tracking
- Cross-asset correlation analysis
- Equal-weight portfolio simulation
- Drawdown & risk metrics

Designed using **dbt + DuckDB + Streamlit** for analytical performance workflows.
""")

# ==========================================================
# 8️⃣ Summary Metrics
# ==========================================================

st.subheader("Summary Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Avg Daily Return", f"{df['daily_return'].mean():.4%}")
col3.metric("Avg 30D Volatility", f"{df['volatility_30d'].mean():.2%}")

# ==========================================================
# Charts
# ==========================================================

def percent_axis(fig):
    fig.update_yaxes(tickformat=".2%")
    return fig

# Daily Return
st.subheader("Daily Return")
st.plotly_chart(
    percent_axis(px.line(df, x="date", y="daily_return", color="asset")),
    width="stretch"
)

# 7D MA
st.subheader("7-Day Moving Average")
st.plotly_chart(
    percent_axis(px.line(df, x="date", y="daily_return_7d_ma", color="asset")),
    width="stretch"
)

# Cumulative Return
st.subheader("Cumulative Return (Growth of $1)")
st.plotly_chart(
    px.line(df, x="date", y="cumulative_return", color="asset"),
    width="stretch"
)

# Volatility
st.subheader("30-Day Rolling Volatility (Annualized)")
st.plotly_chart(
    percent_axis(px.line(df, x="date", y="volatility_30d", color="asset")),
    width="stretch"
)

# Sharpe
st.subheader("30-Day Rolling Sharpe Ratio")
st.plotly_chart(
    px.line(df, x="date", y="rolling_sharpe_30d", color="asset"),
    width="stretch"
)

# Log Return
st.subheader("Log Return")
st.plotly_chart(
    percent_axis(px.line(df, x="date", y="log_return", color="asset")),
    width="stretch"
)

# Volume
st.subheader("Volume")
fig_volume = px.line(df, x="date", y="volume", color="asset")
fig_volume.update_yaxes(tickformat=",")
st.plotly_chart(fig_volume, width="stretch")

# ==========================================================
# Correlation
# ==========================================================

st.subheader("Asset Correlation Matrix")

if len(selected_assets) > 1:
    pivot_df = df.pivot(index="date", columns="asset", values="daily_return")
    corr_matrix = pivot_df.corr()

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1
    )
    st.plotly_chart(fig_corr, width="stretch")
else:
    st.info("Select at least two assets to view correlation matrix.")

# ==========================================================
# Portfolio Analytics (Phase 2)
# ==========================================================

if len(selected_assets) > 1:

    st.markdown("---")
    st.header("📊 Portfolio Risk Analytics (Equal Weighted)")

    pivot_returns = df.pivot(index="date", columns="asset", values="daily_return")
    portfolio_return = pivot_returns.mean(axis=1)

    portfolio_df = portfolio_return.to_frame(name="portfolio_return")

    portfolio_df["portfolio_cum_return"] = (1 + portfolio_df["portfolio_return"]).cumprod()
    portfolio_df["rolling_max"] = portfolio_df["portfolio_cum_return"].cummax()
    portfolio_df["drawdown"] = (
        portfolio_df["portfolio_cum_return"] - portfolio_df["rolling_max"]
    ) / portfolio_df["rolling_max"]

    std = portfolio_df["portfolio_return"].std()

    portfolio_ann_vol = std * np.sqrt(365)
    portfolio_sharpe = (
        (portfolio_df["portfolio_return"].mean() / std) * np.sqrt(365)
        if std != 0 else 0
    )

    portfolio_max_dd = portfolio_df["drawdown"].min()

    portfolio_df["rolling_sharpe_30d"] = (
        portfolio_df["portfolio_return"].rolling(30).mean() /
        portfolio_df["portfolio_return"].rolling(30).std()
    ) * np.sqrt(365)

    portfolio_df = portfolio_df.reset_index()

    # Metric Cards
    col1, col2, col3 = st.columns(3)

    col1.metric("Portfolio Sharpe", f"{portfolio_sharpe:.3f}")
    col2.metric("Annualized Volatility", f"{portfolio_ann_vol:.2%}")
    col3.metric("Max Drawdown", f"{portfolio_max_dd:.2%}")

    # Portfolio Charts
    st.subheader("Portfolio Growth")
    st.plotly_chart(
        px.line(portfolio_df, x="date", y="portfolio_cum_return"),
        width="stretch"
    )

    st.subheader("Portfolio Drawdown")
    st.plotly_chart(
        px.line(portfolio_df, x="date", y="drawdown"),
        width="stretch"
    )

    st.subheader("Rolling 30-Day Sharpe")
    st.plotly_chart(
        px.line(portfolio_df, x="date", y="rolling_sharpe_30d"),
        width="stretch"
    )

    # Download Portfolio CSV
    st.subheader("Download Portfolio Data")
    portfolio_csv = portfolio_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Portfolio CSV",
        data=portfolio_csv,
        file_name="portfolio_analytics.csv",
        mime="text/csv"
    )

# ==========================================================
# Download Raw Data
# ==========================================================

st.markdown("---")
st.subheader("Download Filtered Asset Data")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Asset Data CSV",
    data=csv_data,
    file_name="filtered_crypto_data.csv",
    mime="text/csv"
)
