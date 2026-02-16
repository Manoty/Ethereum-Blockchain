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
st.subheader("Summary Metrics")
st.write("Total Records:", len(df))
st.write("Average Daily Return:", f"{df['daily_return'].mean():.6f}")

# ------------------------------
# 7️⃣ Daily Return Plot
# ------------------------------
st.subheader("Daily Return Over Time")
st.markdown("Shows day-to-day returns for the selected assets. Observe volatility and trends.")
fig_return = px.line(
    df,
    x="date",
    y="daily_return",
    color="asset",
    labels={"daily_return": "Daily Return", "date": "Date"},
    title="Daily Return Trends",
    hover_data={"daily_return": ":.4%", "date": "|%Y-%m-%d"}
)
st.plotly_chart(fig_return, width="stretch")

# ------------------------------
# 8️⃣ 7-Day Moving Average Plot
# ------------------------------
st.subheader("7-Day Moving Average of Daily Return")
st.markdown("Smoothed daily returns help identify broader trends and reduce noise.")
fig_ma = px.line(
    df,
    x="date",
    y="daily_return_7d_ma",
    color="asset",
    labels={"daily_return_7d_ma": "7-Day MA Daily Return", "date": "Date"},
    title="Smoothed Daily Return Trends",
    hover_data={"daily_return_7d_ma": ":.4%", "date": "|%Y-%m-%d"}
)
st.plotly_chart(fig_ma, width="stretch")

# ------------------------------
# 9️⃣ Log Return Plot
# ------------------------------
st.subheader("Log Return Over Time")
st.markdown("Log returns are useful for multiplicative returns and risk analysis.")
fig_log = px.line(
    df,
    x="date",
    y="log_return",
    color="asset",
    labels={"log_return": "Log Return", "date": "Date"},
    title="Log Return Trends",
    hover_data={"log_return": ":.4%", "date": "|%Y-%m-%d"}
)
st.plotly_chart(fig_log, width="stretch")

# ------------------------------
# 🔟 Volume Plot
# ------------------------------
st.subheader("Volume Over Time")
st.markdown("Daily trading volume helps understand market activity and liquidity.")
fig_volume = px.line(
    df,
    x="date",
    y="volume",
    color="asset",
    labels={"volume": "Volume", "date": "Date"},
    title="Trading Volume Trends",
    hover_data={"volume": ":,.0f", "date": "|%Y-%m-%d"}
)
st.plotly_chart(fig_volume, width="stretch")

# ------------------------------
# 1️⃣1️⃣ Multi-Metric Toggle Plot with Dual Y-Axis
# ------------------------------
st.subheader("Interactive Multi-Metric Plot (Dual Y-Axis)")
st.markdown("Select multiple metrics to compare returns and volume on the same chart.")

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
                        name=f"{asset} - {metric}",
                        hovertemplate="%{y:,.0f}"
                    ),
                    secondary_y=True
                )
            else:
                fig_multi.add_trace(
                    go.Scatter(
                        x=df_asset['date'],
                        y=df_asset[metric],
                        mode='lines',
                        name=f"{asset} - {metric}",
                        hovertemplate="%{y:.4%}"
                    ),
                    secondary_y=False
                )
    fig_multi.update_layout(
        title_text="Selected Metrics Over Time (Dual Y-Axis)",
        xaxis_title="Date",
        hovermode="x unified"
    )
    if use_secondary_y:
        fig_multi.update_yaxes(title_text="Returns", secondary_y=False)
        fig_multi.update_yaxes(title_text="Volume", secondary_y=True)
    else:
        fig_multi.update_yaxes(title_text="Returns")
    st.plotly_chart(fig_multi, width="stretch")
else:
    st.info("Select at least one metric to display.")

# ------------------------------
# 1️⃣2️⃣ Optional: Download Filtered Data
# ------------------------------
st.subheader("Download Filtered Data")
st.markdown("Download the data you are currently viewing for further analysis.")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="crypto_filtered_data.csv",
    mime="text/csv"
)
