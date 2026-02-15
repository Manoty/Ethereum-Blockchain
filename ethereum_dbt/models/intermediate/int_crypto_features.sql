-- models/intermediate/int_crypto_features.sql

with base as (

    select
        asset,
        date,
        open_price,
        close_price,
        high,
        low,
        volume,

        -- daily return
        case
            when open_price > 0
            then (close_price - open_price) / open_price
            else null
        end as daily_return,

        -- log return
        case
            when open_price > 0
             and close_price > 0
            then ln(close_price / open_price)
            else null
        end as log_return

    from {{ ref('stg_all_crypto') }}

    -- 🔥 CLEAN BAD ROWS
    where open_price > 0
      and close_price > 0
      and volume > 0

),

-- ------------------------------
-- 1️⃣ Add cumulative return
-- ------------------------------
cum as (
    select
        *,
        -- cumulative return: close price divided by first close price in the dataset
        close_price / first_value(close_price) over (partition by asset order by date) - 1 as cum_return
    from base
),

-- ------------------------------
-- 2️⃣ Add rolling metrics
-- ------------------------------
rolling as (
    select
        *,
        -- 7-day rolling volatility
        stddev_samp(daily_return) over (
            partition by asset
            order by date
            rows between 6 preceding and current row
        ) as daily_return_7d_vol,

        -- 7-day rolling Sharpe ratio (assuming risk-free rate ~0)
        case
            when stddev_samp(daily_return) over (
                    partition by asset
                    order by date
                    rows between 6 preceding and current row
                 ) > 0
            then
                avg(daily_return) over (
                    partition by asset
                    order by date
                    rows between 6 preceding and current row
                ) / stddev_samp(daily_return) over (
                    partition by asset
                    order by date
                    rows between 6 preceding and current row
                )
            else null
        end as daily_return_7d_sharpe

    from cum
)

select *
from rolling
order by asset, date
# app.py
import os
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
SELECT date, asset, close_price, open_price, high, low, volume,
       daily_return, log_return,
       cum_return, daily_return_7d_vol, daily_return_7d_sharpe
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
# 5️⃣ Calculate 7-Day Moving Average (if not in db)
# ------------------------------
df = df.sort_values(['asset', 'date'])
if 'daily_return_7d_ma' not in df.columns:
    df['daily_return_7d_ma'] = df.groupby('asset')['daily_return'].transform(lambda x: x.rolling(7, min_periods=1).mean())

# ------------------------------
# 6️⃣ Dashboard Title & Summary
# ------------------------------
st.title("📊 Crypto Daily Metrics Dashboard")
st.markdown("""
**Description:** Explore daily crypto metrics including returns, cumulative performance, volatility, and rolling Sharpe ratio.
Select assets and date ranges to filter the dashboard.
""")

st.subheader("Summary Metrics")
st.write("Total Records:", len(df))
st.write("Average Daily Return:", round(df['daily_return'].mean(), 6))

# ------------------------------
# 7️⃣ Daily Return Plot
# ------------------------------
st.subheader("Daily Return Over Time")
st.markdown("Shows each asset's daily percentage return.")
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
st.markdown("Smoothed trends of daily return to identify short-term momentum.")
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
st.markdown("Continuous compounding log returns for each asset.")
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
st.markdown("Daily trading volume for selected assets.")
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
st.markdown("Select any combination of metrics to view returns and volume on the same chart.")

metrics = st.multiselect(
    "Select Metrics to Display",
    options=["daily_return", "daily_return_7d_ma", "log_return", "volume", "cum_return", "daily_return_7d_vol", "daily_return_7d_sharpe"],
    default=["daily_return", "daily_return_7d_ma"]
)

if metrics:
    use_secondary_y = any(m in ["volume"] for m in metrics)
    fig_multi = make_subplots(specs=[[{"secondary_y": use_secondary_y}]])

    for metric in metrics:
        for asset in df['asset'].unique():
            df_asset = df[df['asset'] == asset]
            sec_y = True if metric == "volume" else False
            fig_multi.add_trace(
                go.Scatter(
                    x=df_asset['date'],
                    y=df_asset[metric],
                    mode='lines',
                    name=f"{asset} - {metric}"
                ),
                secondary_y=sec_y
            )

    fig_multi.update_layout(
        title_text="Selected Metrics Over Time (Dual Y-Axis)",
        xaxis_title="Date"
    )

    if use_secondary_y:
        fig_multi.update_yaxes(title_text="Returns / Other Metrics", secondary_y=False)
        fig_multi.update_yaxes(title_text="Volume", secondary_y=True)
    else:
        fig_multi.update_yaxes(title_text="Returns / Other Metrics")

    st.plotly_chart(fig_multi, width="stretch")
else:
    st.info("Select at least one metric to display.")

# ------------------------------
# 1️⃣2️⃣ Optional: Download Filtered Data
# ------------------------------
st.subheader("Download Filtered Data")
st.markdown("Download the currently filtered data as CSV for offline analysis.")
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False),
    file_name="crypto_filtered_data.csv",
    mime="text/csv"
)
