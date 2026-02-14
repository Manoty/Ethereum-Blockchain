import duckdb
import streamlit as st

conn = duckdb.connect("dev.duckdb", read_only=True)

df = conn.execute("""
    SELECT *
    FROM int_crypto_features
    LIMIT 10
""").df()

st.write(df)
