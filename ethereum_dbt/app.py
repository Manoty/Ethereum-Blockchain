# app.py
import streamlit as st
import duckdb
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
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

assets_df = conn.execute(
    "SELECT DISTINCT asset FROM int_crypto_features ORDER BY asset"
).df()

all_assets = assets_df['asset'].tolist()

selected_assets = st.sidebar.multiselect(
    "Select Assets",
    all_assets,
    default=all_assets[:5]
)

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

# ------------------------------
# 3️⃣ Query Filtered Data
# ------------------------------
query = f"""
SELECT date, asset, close_price, open_price, high, low,
       volume, daily_return, log_return
FROM int_crypto_features
WHERE asset IN ({','.join([f"'{a}'" for a in selected_assets])})
  AND date BETWEEN '{start_date_str}' AND '{end_date_str}'
ORDER BY asset, date
"""

df = conn.execute(query).df()

# ------------------------------
# 4️⃣ Data Cleaning
# ------------------------------
df.columns = [c.lower() for c in df.columns]
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['asset', 'date'])

# ------------------------------
# 5️⃣ Feature Engineering
# ------------------------------

df['daily_return_7d_ma'] = (
    df.groupby('asset')['daily_return']
    .transform(lambda x: x.rolling(7, min_periods=1).mean())
)

df['cumulative_return'] = (
    df.groupby('asset')['daily_return']
    .transform(lambda x: (1 + x).cumprod())
)

df['volatility_30d'] = (
    df.groupby('asset')['daily_return']
    .transform(lambda x: x.rolling(30, min_periods=5).std() * np.sqrt(365))
)

df['rolling_mean_30d'] = (
    df.groupby('asset')['daily_return']
    .transform(lambda x: x.rolling(30, min_periods=5).mean())
)

df['rolling_sharpe_30d'] = (
    df['rolling_mean_30d'] /
    (df['volatility_30d'] / np.sqrt(365))
)

# ------------------------------
# 6️⃣ Dashboard Title
# ------------------------------
st.title("📊 Crypto Performance & Risk Analytics Dashboard")

st.markdown("""
This dashboard provides performance, risk, and cross-asset analytics for selected cryptocurrencies.
Metrics include returns, smoothed trends, cumulative growth, volatility, Sharpe ratio,
and asset correlations.
""")

# ------------------------------
# Summary Metrics
# ------------------------------
st.subheader("Summary Metrics")

st.write("Total Records:", len(df))
st.write("Average Daily Return:", round(df['daily_return'].mean(), 6))
st.write("Average 30D Volatility:", round(df['volatility_30d'].mean(), 4))
st.write("Average 30D Sharpe:", round(df['rolling_sharpe_30d'].mean(), 4))

# ------------------------------
# Daily Return
# ------------------------------
st.subheader("Daily Return Over Time")
st.markdown("Shows the raw day-to-day percentage change in price for each selected asset.")

fig_return = px.line(df, x="date", y="daily_return", color="asset")
fig_return.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_return, width="stretch")

# ------------------------------
# 7-Day MA
# ------------------------------
st.subheader("7-Day Moving Average of Daily Return")
st.markdown("Smooths short-term noise to highlight recent return trends.")

fig_ma = px.line(df, x="date", y="daily_return_7d_ma", color="asset")
fig_ma.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_ma, width="stretch")

# ------------------------------
# Cumulative Return
# ------------------------------
st.subheader("Cumulative Return (Growth of $1 Invested)")
st.markdown("Represents how $1 would have grown over time based on compounded daily returns.")

fig_cum = px.line(df, x="date", y="cumulative_return", color="asset")
st.plotly_chart(fig_cum, width="stretch")

# ------------------------------
# Volatility
# ------------------------------
st.subheader("30-Day Rolling Volatility (Annualized)")
st.markdown("Measures rolling risk using the standard deviation of daily returns, annualized.")

fig_vol = px.line(df, x="date", y="volatility_30d", color="asset")
fig_vol.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_vol, width="stretch")

# ------------------------------
# Sharpe Ratio
# ------------------------------
st.subheader("30-Day Rolling Sharpe Ratio (Annualized)")
st.markdown("Risk-adjusted performance metric. Higher values indicate better return per unit of risk.")

fig_sharpe = px.line(df, x="date", y="rolling_sharpe_30d", color="asset")
st.plotly_chart(fig_sharpe, width="stretch")

# ------------------------------
# Log Return
# ------------------------------
st.subheader("Log Return Over Time")
st.markdown("Logarithmic returns are additive and commonly used in quantitative modeling.")

fig_log = px.line(df, x="date", y="log_return", color="asset")
fig_log.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_log, width="stretch")

# ------------------------------
# Volume
# ------------------------------
st.subheader("Volume Over Time")
st.markdown("Displays traded volume to help analyze liquidity and market activity.")

fig_volume = px.line(df, x="date", y="volume", color="asset")
fig_volume.update_yaxes(tickformat=",")
st.plotly_chart(fig_volume, width="stretch")

# ==========================================================
# 🚀 PHASE 2 — Portfolio Risk Analytics
# ==========================================================

if len(selected_assets) > 1:

    st.markdown("---")
    st.header("📊 Portfolio Risk Analytics (Equal Weighted)")

    st.markdown("""
This section builds an equal-weighted portfolio from selected assets.
It calculates cumulative growth, volatility, Sharpe ratio, and drawdowns
to evaluate portfolio-level risk and performance.
""")

    pivot_returns = df.pivot(index='date', columns='asset', values='daily_return')
    portfolio_daily_return = pivot_returns.mean(axis=1)
    portfolio_df = portfolio_daily_return.to_frame(name='portfolio_return')

    portfolio_df['portfolio_cum_return'] = (1 + portfolio_df['portfolio_return']).cumprod()
    portfolio_df['rolling_max'] = portfolio_df['portfolio_cum_return'].cummax()

    portfolio_df['drawdown'] = (
        portfolio_df['portfolio_cum_return'] - portfolio_df['rolling_max']
    ) / portfolio_df['rolling_max']

    portfolio_ann_vol = portfolio_df['portfolio_return'].std() * np.sqrt(365)

    portfolio_sharpe = (
        portfolio_df['portfolio_return'].mean() /
        portfolio_df['portfolio_return'].std()
    ) * np.sqrt(365)

    portfolio_max_dd = portfolio_df['drawdown'].min()

    portfolio_df['rolling_sharpe_30d'] = (
        portfolio_df['portfolio_return']
        .rolling(30)
        .mean()
        / portfolio_df['portfolio_return'].rolling(30).std()
    ) * np.sqrt(365)

    portfolio_df = portfolio_df.reset_index()

    # Metric Cards
    col1, col2, col3 = st.columns(3)

    col1.metric("Portfolio Sharpe Ratio", round(portfolio_sharpe, 3))
    col2.metric("Annualized Volatility", f"{round(portfolio_ann_vol * 100, 2)}%")
    col3.metric("Max Drawdown", f"{round(portfolio_max_dd * 100, 2)}%")

    # Portfolio Cumulative
    st.subheader("Portfolio Cumulative Return")
    st.markdown("Shows growth of an equal-weighted portfolio over time.")

    fig_port_cum = px.line(portfolio_df, x='date', y='portfolio_cum_return')
    st.plotly_chart(fig_port_cum, width="stretch")

    # Drawdown
    st.subheader("Portfolio Drawdown")
    st.markdown("Measures peak-to-trough decline. Highlights risk during downturns.")

    fig_dd = px.line(portfolio_df, x='date', y='drawdown')
    st.plotly_chart(fig_dd, width="stretch")

    # Rolling Sharpe
    st.subheader("Portfolio Rolling 30-Day Sharpe")
    st.markdown("Shows how risk-adjusted performance evolves over time.")

    fig_roll = px.line(portfolio_df, x='date', y='rolling_sharpe_30d')
    st.plotly_chart(fig_roll, width="stretch")
