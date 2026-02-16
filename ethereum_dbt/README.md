📊 Ethereum & Crypto Analytics Dashboard

A Streamlit-powered interactive dashboard for analyzing cryptocurrency daily metrics. Built on DuckDB, Pandas, and Plotly, this dashboard provides insights into asset returns, volatility, correlations, and risk-adjusted performance.

🚀 Features

Daily Return Analysis – visualize day-to-day performance trends.

7-Day Moving Average – smooth out noise to identify trends.

Log Returns – for multiplicative return analysis.

Trading Volume Visualization – track liquidity and market activity.

Multi-Metric Interactive Plot – compare multiple metrics with dual Y-axis support.

Rolling Sharpe Ratio – assess risk-adjusted returns.

Correlation Heatmap – examine relationships between asset returns.

Download Filtered Data – export selected datasets as CSV.

Fully interactive date and asset selection.

🛠 Technology Stack

Python 3.11

Streamlit – front-end dashboard interface

DuckDB – local analytical database

Pandas & NumPy – data wrangling & calculations

Plotly – interactive visualizations

Plotly Express / Graph Objects – line charts, dual-axis plots, heatmaps

📂 Project Structure
ethereum_dbt/
├─ app.py                 # Streamlit dashboard main app
├─ data.py                # Optional data utilities
├─ dev.duckdb             # DuckDB database (local)
├─ models/                # dbt models
├─ seeds/                 # Seed CSV data
├─ snapshots/             # dbt snapshots
├─ sources/               # dbt sources
├─ tests/                 # dbt tests
├─ requirements.txt       # Python dependencies
└─ README.md              # This file

⚡ Installation & Running

Clone the repo

git clone <repo-url>
cd ethereum_dbt


Create and activate virtual environment

python -m venv venv
source venv/bin/activate       # Linux / Mac
venv\Scripts\activate          # Windows


Install dependencies

pip install -r requirements.txt


Run Streamlit app

streamlit run app.py

🎛 Usage

Select one or more cryptocurrencies from the sidebar.

Pick a date range to filter the data.

Explore the charts: Daily Returns, Log Returns, Volume, 7-day MA.

Use the multi-metric plot to compare multiple metrics.

Check risk-adjusted performance using the rolling Sharpe ratio.

Explore asset correlations via the heatmap.

Download the filtered data for offline analysis.



📝 Contributing

Pull requests are welcome.

Please update tests and documentation as needed.

Ensure DuckDB files are available locally to run the app.

⚠️ Notes

Database (dev.duckdb) is not included in GitHub.

Ensure dependencies match requirements.txt.

Tested on Python 3.11 and Streamlit 1.54.0.