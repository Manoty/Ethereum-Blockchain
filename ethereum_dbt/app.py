import streamlit as st
import duckdb
import pandas as pd
import datetime

# Connect to your DuckDB database
conn = duckdb.connect('eth_blockchain.duckdb')

# Example: choose start and end dates via Streamlit date_input
start_date = st.date_input("Start Date", datetime.date(2014, 9, 18))
end_date   = st.date_input("End Date", datetime.date(2014, 9, 19))

# Convert to ISO format (YYYY-MM-DD) for SQL
start_str = start_date.isoformat()
end_str   = end_date.isoformat()

# Build your query safely
query = f"""
SELECT
    date,
    asset,
    close_price,
    open_price,
    high_price,
    low_price,
    volume,
    daily_return,
    log_return
FROM eth_prices
WHERE date BETWEEN '{start_str}' AND '{end_str}'
ORDER BY date
LIMIT 100
"""

# Execute and fetch results as DataFrame
df = conn.execute(query).df()

# Show in Streamlit
st.write(df)
