import os
import duckdb
import streamlit as st

db_path = r"C:\kev\Ethereum_Blockchain\eth_blockchain\ethereum_dbt\dev.duckdb"

st.write("Database path:", db_path)
st.write("File exists:", os.path.exists(db_path))

conn = duckdb.connect(db_path, read_only=True)

count = conn.execute("SELECT COUNT(*) FROM int_crypto_features").fetchone()[0]
st.write("Row count in int_crypto_features:", count)
