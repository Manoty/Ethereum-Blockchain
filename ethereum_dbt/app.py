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

assets_df = conn.execute(
    "SELECT DISTINCT asset FROM int_crypto_features ORDER BY asset"
).df()
all_assets = assets_df['asset'].tolist()

selected_assets = st.sidebar.multiselect(
    "Select Assets", all_assets, default=all_assets[:5]
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

# 7-Day Moving Average
df['daily_return_7d_ma'] = (
    df.groupby('asset')['daily_return']
    .transform(lambda x: x.rolling(7, min_periods=1).mean())
)

# ✅ Cumulative Return (Growth of $1)
df['cumulative_return'] = (
    df.groupby('asset')['daily_return']
    .transform(lambda x: (1 + x).cumprod())
)

# ------------------------------
# 6️⃣ Dashboard Title & Description
# ------------------------------
st.title("📊 Crypto Daily Metrics Dashboard")
st.markdown(
    """
    Interactive dashboard for analyzing crypto asset performance.
    View daily returns, smoothed trends, cumulative growth,
    log returns, volume, and per-asset sparkline summaries.
    """
)

st.subheader("Summary Metrics")
st.write("Total Records:", len(df))
st.write("Average Daily Return:", round(df['daily_return'].mean(), 6))

# ------------------------------
# 7️⃣ Daily Return Plot
# ------------------------------
st.subheader("Daily Return Over Time")
fig_return = px.line(df, x="date", y="daily_return", color="asset")
fig_return.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_return, width="stretch")

# ------------------------------
# 8️⃣ 7-Day Moving Average Plot
# ------------------------------
st.subheader("7-Day Moving Average of Daily Return")
fig_ma = px.line(df, x="date", y="daily_return_7d_ma", color="asset")
fig_ma.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_ma, width="stretch")

# ------------------------------
# 🆕 9️⃣ Cumulative Return Plot
# ------------------------------
st.subheader("Cumulative Return (Growth of $1 Invested)")
st.markdown(
    "Shows how $1 would have grown over time based on daily returns."
)

fig_cum = px.line(
    df,
    x="date",
    y="cumulative_return",
    color="asset"
)
fig_cum.update_yaxes(tickformat=".2f")
st.plotly_chart(fig_cum, width="stretch")

# ------------------------------
# 🔟 Log Return Plot
# ------------------------------
st.subheader("Log Return Over Time")
fig_log = px.line(df, x="date", y="log_return", color="asset")
fig_log.update_yaxes(tickformat=".2%")
st.plotly_chart(fig_log, width="stretch")

# ------------------------------
# 1️⃣1️⃣ Volume Plot
# ------------------------------
st.subheader("Volume Over Time")
fig_volume = px.line(df, x="date", y="volume", color="asset")
fig_volume.update_yaxes(tickformat=",")
st.plotly_chart(fig_volume, width="stretch")

# ------------------------------
# 1️⃣2️⃣ Multi-Metric Toggle Plot
# ------------------------------
st.subheader("Interactive Multi-Metric Plot (Dual Y-Axis)")

metrics = st.multiselect(
    "Select Metrics",
    options=[
        "daily_return",
        "daily_return_7d_ma",
        "cumulative_return",
        "log_return",
        "volume"
    ],
    default=["daily_return", "cumulative_return"]
)

if metrics:
    use_secondary_y = "volume" in metrics
    fig_multi = make_subplots(specs=[[{"secondary_y": use_secondary_y}]])

    for metric in metrics:
        for asset in df['asset'].unique():
            df_asset = df[df['asset'] == asset]

            fig_multi.add_trace(
                go.Scatter(
                    x=df_asset['date'],
                    y=df_asset[metric],
                    mode='lines',
                    name=f"{asset} - {metric}"
                ),
                secondary_y=(metric == "volume")
            )

    if use_secondary_y:
        fig_multi.update_yaxes(title_text="Returns", secondary_y=False)
        fig_multi.update_yaxes(title_text="Volume", secondary_y=True)

    st.plotly_chart(fig_multi, width="stretch")
else:
    st.info("Select at least one metric to display.")

# ------------------------------
# 1️⃣3️⃣ Portfolio Sparklines
# ------------------------------
st.subheader("Portfolio Sparklines by Asset")

for asset in selected_assets:
    df_asset = df[df['asset'] == asset]
    if df_asset.empty:
        continue

    fig_spark = go.Figure()

    fig_spark.add_trace(go.Scatter(
        x=df_asset['date'],
        y=df_asset['daily_return'],
        mode='lines',
        line=dict(width=2),
        showlegend=False
    ))

    fig_spark.update_layout(
        height=150,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showticklabels=False),
        yaxis=dict(tickformat=".2%")
    )

    st.plotly_chart(fig_spark, width="stretch")

# ------------------------------
# 1️⃣4️⃣ Download CSV
# ------------------------------
st.subheader("Download Filtered Data")

csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="filtered_crypto_data.csv",
    mime="text/csv"
)

