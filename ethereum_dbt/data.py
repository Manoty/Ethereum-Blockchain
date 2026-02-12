import duckdb
import os

# Directory where you saved CSVs
csv_dir = "datasets"  # e.g., datasets/blocks.csv, datasets/transactions.csv

# Connect to DuckDB
con = duckdb.connect("ethereum_local.duckdb")

# List of CSV files to load
csv_files = {
    "blocks": "blocks.csv",
    "transactions": "transactions.csv",
    "token_transfers": "token_transfers.csv"
}

# Load CSVs into DuckDB
for table, file_name in csv_files.items():
    path = os.path.join(csv_dir, file_name)
    if os.path.exists(path):
        print(f"Loading {file_name} into table {table}")
        con.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} AS
            SELECT * FROM read_csv_auto('{path}');
        """)
    else:
        print(f"File {file_name} not found in {csv_dir}, skipping.")

print("All available CSVs loaded into DuckDB.")
