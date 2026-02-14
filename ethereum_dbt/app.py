# app.py
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# 6️⃣ Dashboard Title, Short Description & Summary
# ------------------------------
st.title("📊 Crypto Daily Metrics Dashboard")

st.markdown(
    """
    **Quick overview:** This dashboard shows per-asset daily performance and volume trends.
    - Use the sidebar to choose assets and a date range.  
    - The charts below include raw daily returns, a 7-day moving average (smoother trend), log returns, and trading volume.
    - Use the interactive multi-metric plot to compare different metrics on one chart (volume will be shown on a secondary axis).
    """
)

st.subheader("Summary Metrics")
st.write("Total Records:", len(df))
st.write("Average Daily Return:", round(df['daily_return'].mean(), 6))

# ------------------------------
# 7️⃣ Daily Return Plot
# ------------------------------
st.markdown("**Daily Return Over Time** — shows the day-to-day percentage change `((close - open)/open)` for each selected asset.")
fig_return = px.line(
    df,
    x="date",
    y="daily_return",
    color="asset",
    labels={"daily_return": "Daily Return", "date": "Date"},
    title="Daily Return Trends",
    hover_data={
        "daily_return": ":.2%",
        "date": "|%Y-%m-%d",
        "asset": True
    }
)
fig_return.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_return, width="stretch")

# ------------------------------
# 8️⃣ 7-Day Moving Average Plot
# ------------------------------
st.markdown("**7-Day Moving Average** — the 7-day rolling mean of daily returns. Use this to see smoother trends and reduce noise.")
fig_ma = px.line(
    df,
    x="date",
    y="daily_return_7d_ma",
    color="asset",
    labels={"daily_return_7d_ma": "7-Day MA Daily Return", "date": "Date"},
    title="Smoothed Daily Return Trends",
    hover_data={
        "daily_return_7d_ma": ":.2%",
        "date": "|%Y-%m-%d",
        "asset": True
    }
)
fig_ma.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_ma, width="stretch")

# ------------------------------
# 9️⃣ Log Return Plot
# ------------------------------
st.markdown("**Log Return** — the continuous return `ln(close/open)`. Useful for certain risk calculations and aggregation.")
fig_log = px.line(
    df,
    x="date",
    y="log_return",
    color="asset",
    labels={"log_return": "Log Return", "date": "Date"},
    title="Log Return Trends",
    hover_data={
        "log_return": ":.2%",
        "date": "|%Y-%m-%d",
        "asset": True
    }
)
fig_log.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_log, width="stretch")

# ------------------------------
# 🔟 Volume Plot
# ------------------------------
st.markdown("**Volume Over Time** — trading volume per asset. Often used to confirm the strength of price moves.")
fig_volume = px.line(
    df,
    x="date",
    y="volume",
    color="asset",
    labels={"volume": "Volume", "date": "Date"},
    title="Trading Volume Trends",
    hover_data={
        "volume": ":,",
        "date": "|%Y-%m-%d",
        "asset": True
    }
)
fig_volume.update_yaxes(tickformat=",")
st.plotly_chart(fig_volume, width="stretch")

# ------------------------------
# 1️⃣1️⃣ Multi-Metric Toggle Plot with Dual Y-Axis
# ------------------------------
st.markdown("**Interactive Multi-Metric Chart** — pick metrics to overlay. Volume appears on the secondary axis when selected.")
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
            hover_fmt = ":.2%" if "return" in metric else ":,"
            fig_multi.add_trace(
                go.Scatter(
                    x=df_asset['date'],
                    y=df_asset[metric],
                    mode='lines',
                    name=f"{asset} - {metric}",
                    hovertemplate=f"%{{x|%Y-%m-%d}}<br>{metric}: %{{y{hover_fmt}}}<br>Asset: {asset}"
                ),
                secondary_y=(metric == "volume")
            )

    fig_multi.update_layout(
        title_text="Selected Metrics Over Time (Dual Y-Axis)",
        xaxis_title="Date"
    )

    if use_secondary_y:
        fig_multi.update_yaxes(title_text="Returns", secondary_y=False, tickformat=".2%")
        fig_multi.update_yaxes(title_text="Volume", secondary_y=True, tickformat=",")
    else:
        fig_multi.update_yaxes(title_text="Returns", tickformat=".2%")

    st.plotly_chart(fig_multi, width="stretch")
else:
    st.info("Select at least one metric to display.")

# ------------------------------
# 1️⃣2️⃣ Portfolio Sparklines per Asset (Conditional Coloring)
# ------------------------------
st.markdown("**Sparklines by Asset** — compact daily-return mini-charts. Green = positive day, Red = negative day.")
for asset in selected_assets:
    df_asset = df[df['asset'] == asset].sort_values("date")
    if df_asset.empty:
        continue

    # Split into positive and negative returns
    pos_df = df_asset[df_asset['daily_return'] >= 0]
    neg_df = df_asset[df_asset['daily_return'] < 0]

    fig_spark = go.Figure()

    # Positive returns in green
    fig_spark.add_trace(go.Scatter(
        x=pos_df['date'],
        y=pos_df['daily_return'],
        mode='lines',
        line=dict(color='green', width=2),
        hovertemplate="%{x|%Y-%m-%d}<br>Daily Return: %{y:.2%}<extra></extra>"
    ))

    # Negative returns in red
    fig_spark.add_trace(go.Scatter(
        x=neg_df['date'],
        y=neg_df['daily_return'],
        mode='lines',
        line=dict(color='red', width=2),
        hovertemplate="%{x|%Y-%m-%d}<br>Daily Return: %{y:.2%}<extra></extra>"
    ))

    fig_spark.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=150,
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=True, tickformat=".2%")
    )

    st.plotly_chart(fig_spark, width="stretch")

# ------------------------------
# 1️⃣3️⃣ Download Filtered Data
# ------------------------------
st.subheader("Download Filtered Data")
st.markdown("Download the currently filtered dataset (CSV) for offline analysis or sharing.")
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="filtered_crypto_data.csv",
    mime="text/csv"
)
