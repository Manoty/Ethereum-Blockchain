📊 Crypto Performance & Risk Analytics Dashboard

A quantitative crypto analytics dashboard built with Streamlit, DuckDB, Pandas, and Plotly.

This project delivers performance analysis, volatility modeling, correlation insights, and portfolio-level risk analytics using engineered financial features.

🚀 Overview

This dashboard allows users to:

Select multiple crypto assets

Filter by custom date ranges

Analyze return behavior

Measure rolling volatility

Evaluate Sharpe ratios

Visualize cross-asset correlations

Build an equal-weighted portfolio

Analyze drawdowns and risk metrics

Export filtered datasets

The system is backed by a DuckDB analytical database built from a dbt pipeline.

🏗️ Architecture

Data Layer

dbt transformations

DuckDB analytics warehouse (dev.duckdb)

Feature engineering models

Analytics Layer

Rolling statistics

Cumulative returns

Volatility modeling

Sharpe ratio computation

Correlation matrix

Portfolio risk metrics

Application Layer

Streamlit dashboard

Plotly interactive visualizations

📂 Project Structure
ethereum_dbt/
│
├── app.py
├── dev.duckdb
├── models/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── seeds/
├── dbt_project.yml
├── requirements.txt
└── README.md

📈 Analytics & Metrics
Asset-Level Metrics

Daily Return

7-Day Moving Average Return

Cumulative Return (Growth of $1)

30-Day Rolling Volatility (Annualized)

30-Day Rolling Sharpe Ratio

Log Returns

Trading Volume

Correlation Matrix

📊 Portfolio Risk Analytics (Equal Weighted)

When multiple assets are selected, the dashboard automatically builds an equal-weighted portfolio.

Portfolio metrics include:

Portfolio Cumulative Return

Annualized Volatility

Sharpe Ratio

Rolling 30-Day Sharpe

Maximum Drawdown

Drawdown Time Series

🧠 Risk Metric Definitions

Volatility (Annualized)
Standard deviation of daily returns scaled by √365.

Sharpe Ratio
Risk-adjusted return metric:

(mean portfolio return / std deviation) × √365


Drawdown
Peak-to-trough decline in portfolio value.

Max Drawdown
Largest observed drawdown during selected period.

🛠️ Tech Stack

Python 3.10+

Streamlit

DuckDB

dbt

Pandas

NumPy

Plotly

⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/crypto-risk-dashboard.git
cd crypto-risk-dashboard

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run dbt (if rebuilding database)
dbt run

4️⃣ Launch App
streamlit run app.py

📦 Data Source

The DuckDB database is generated via dbt transformations from structured crypto price data.

Core table used:

int_crypto_features


Includes:

close_price

daily_return

log_return

volume

engineered rolling features

📊 Features Engineered

Rolling mean returns

Rolling volatility (30D)

Rolling Sharpe (30D)

7-day smoothed returns

Cumulative return curves

Portfolio drawdown tracking

📤 Export Capability

Users can download filtered data directly from the dashboard as a CSV file.

🌍 Deployment

Deployable on:

Streamlit Community Cloud

Render

Railway

Docker environments

Ensure dev.duckdb is included in deployment root.

🗺️ Roadmap
Phase 1 (Completed)

Asset-level analytics

Rolling risk metrics

Correlation matrix

Equal-weighted portfolio

Drawdown analysis

Phase 2 (In Progress / Optional Expansion)

Value at Risk (VaR)

Sortino Ratio

Beta vs BTC

Efficient Frontier

Monte Carlo simulation

Risk-adjusted ranking system

📌 Future Enhancements

Custom portfolio weights

Risk-free rate input

Backtesting engine

Strategy comparison framework

Factor modeling

Regime detection

API integration for live pricing

📜 License

MIT License

👤 Author

Built as a quantitative analytics engineering project combining:

Data modeling

Financial risk analytics

Portfolio theory

Interactive dashboard engineering
