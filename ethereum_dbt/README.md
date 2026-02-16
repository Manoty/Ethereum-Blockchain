📈 Crypto Analytics Dashboard

A fully interactive Streamlit dashboard for analyzing cryptocurrency daily metrics, built on DuckDB, Pandas, and Plotly. Explores asset returns, volatility, correlations, and risk-adjusted performance for multiple assets in one place.

This project demonstrates data engineering, analytics, and visualization skills for portfolio and professional use.

💡 Key Features

Daily Return Analysis – visualize daily gains and losses per asset.

7-Day Moving Average – smooth out short-term fluctuations.

Log Returns – measure multiplicative changes.

Trading Volume Insights – analyze liquidity and market activity trends.

Multi-Metric Interactive Plot – compare multiple metrics simultaneously with dual Y-axis support.

Rolling Sharpe Ratio – assess risk-adjusted performance dynamically.

Correlation Heatmap – identify relationships and dependencies between assets.

Download Filtered Data – export selected datasets for offline analysis.

Each visualization includes hover tooltips, formatted axes, and labels for readability.

🔧 Tech Stack

Python 3.11

Streamlit – interactive dashboard interface

DuckDB – local analytical database for fast queries

Pandas & NumPy – data wrangling and calculations

Plotly – interactive visualizations (line charts, dual-axis plots, heatmaps)

🗂 Project Structure
ethereum_dbt/
├─ app.py                 # Main Streamlit dashboard
├─ data.py                # Data utility functions
├─ dev.duckdb             # Local DuckDB database (not in GitHub)
├─ models/                # dbt models for feature engineering
├─ seeds/                 # Seed CSVs for dbt
├─ snapshots/             # dbt snapshots
├─ sources/               # dbt sources
├─ tests/                 # dbt tests
├─ requirements.txt       # Python dependencies
└─ README.md              # This file

🚀 Installation & Run

Clone the repository:

git clone <repo-url>
cd ethereum_dbt


Set up a virtual environment:

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Launch the dashboard:

streamlit run app.py



🎛 How to Use

Select assets from the sidebar.

Pick a date range to filter data.

Explore the interactive charts:

Daily Returns

7-Day Moving Average

Log Returns

Trading Volume

Multi-Metric Dual Y-Axis Plot

Rolling Sharpe Ratio

Correlation Heatmap

Download filtered data as CSV for offline analysis.

Each chart provides tooltips, formatted axes, and legends for quick understanding.



📌 Notes

dev.duckdb is not included in the repository. Place it in the project root to run locally.

Tested on Python 3.11, Streamlit 1.54, DuckDB 1.4+.