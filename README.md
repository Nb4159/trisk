# AI-Driven Financial Risk Engine

A modular quantitative finance and synthetic market simulation platform focused on:

* Volatility Forecasting
* Portfolio Risk Analysis
* Monte Carlo Simulation
* Synthetic Financial Data Generation
* Scenario-Based Market Modeling
* AI-Driven Sentiment Analysis

This project combines traditional quantitative finance techniques such as GARCH models, Monte Carlo simulations, and risk metrics with modern generative AI approaches including VAEs, GANs, Diffusion Models, and LLM-based financial sentiment systems.

The long-term objective is to build a realistic financial simulation environment capable of modeling how macroeconomic events, geopolitical shocks, corporate fundamentals, and sentiment changes affect market behavior.

---

# Current Features

## Phase 1 — Historical Risk Analytics ✅

* Financial data ingestion using Yahoo Finance
* Log return calculation
* Rolling volatility estimation
* Sharpe ratio computation
* GARCH volatility forecasting
* ACF/PACF diagnostics
* Parquet-based data storage
* MLflow experiment tracking
* Dockerized development environment
* Config-driven pipelines

---

## Phase 2 — Market Simulation & Risk Engine ✅

### 2.1 — Simulation Engine
* Geometric Brownian Motion (GBM) simulation
* GARCH-conditioned Monte Carlo (dynamic volatility per timestep)
* Antithetic variates for variance reduction
* Interactive simulation visualizations (Plotly)
* Parquet-based forecast storage

### 2.2 — Risk Metrics
* Value at Risk (VaR) — historical, parametric, Monte Carlo
* Conditional Value at Risk (CVaR / Expected Shortfall)
* Dollar VaR
* Max drawdown and recovery period analysis
* Probability of loss, probability of target gain/loss

### 2.3 — Backtesting
* Rolling historical VaR backtesting (252-day window)
* Kupiec proportion of failures test
* Violation rate reporting

---

## Validation Results

| Ticker | Asset Type | VaR 95% | CVaR 95% | Max Drawdown | Kupiec P-value | Passed |
|--------|------------|---------|----------|--------------|----------------|--------|
| SPY | US Index ETF | 0.35% | 0.44% | -0.20% | 0.9897 | ✅ |
| DIS | Media/Entertainment | 0.86% | 1.07% | -0.53% | 0.7006 | ✅ |
| TSLA | High Vol Growth | 1.47% | 1.85% | -0.83% | 0.6907 | ✅ |
| GME | Meme Stock | 1.98% | 2.49% | -1.11% | 0.6907 | ✅ |
| LUNA-USD | Collapsed Crypto | 84.0% | 88.5% | -58.46% | 0.7049 | ✅ |

Model correctly identifies risk spectrum from near-riskless (SPY) to catastrophic (LUNA),
with Kupiec backtesting passing across all asset classes.

---

## Phase 3 — Multi-Asset Portfolio (In Progress) 🚧

* Portfolio VaR and CVaR
* Correlation matrix estimation
* Covariance-based risk decomposition
* Portfolio-level Monte Carlo simulation

# Example Output

```text
Sharpe Ratio: 0.7882748057356007

Forecasted Volatility:
[1.90613251 1.97717036 2.04536768 2.11083806 2.17369054]
```

Example Monte Carlo statistics:

```text
Mean Future Price
Median Future Price
5th Percentile Price
95th Percentile Price
Probability of Loss
Value at Risk (VaR)
```

---

# Tech Stack

### Core

* Python
* FastAPI (Planned)
* Docker

### Data & Storage

* DuckDB
* SQLite
* Parquet

### Quantitative Finance

* NumPy
* Pandas
* ARCH (GARCH Models)
* Monte Carlo Simulation

### Machine Learning

* PyTorch
* Scikit-Learn

### Experiment Tracking

* MLflow
* Weights & Biases (Planned)

### Visualization

* Plotly
* Matplotlib

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Nb4159/trisk.git
cd trisk
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv fna
fna\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv fna
source fna/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Volatility Forecasting Pipeline

```bash
python pipelines/garch_pipeline.py \
    --config configs/base.yaml
```

---

## Monte Carlo Simulation Pipeline

```bash
python pipelines/garch_simulate.py \
    --config configs/base.yaml
```

---

## Run MLflow

```bash
mlflow ui --host 0.0.0.0 --port 5000
```

Open:

```text
http://localhost:5000
```

---

## Run Docker Environment

```bash
docker compose build
docker compose up
```

---

# Project Roadmap

## Phase 2.1 — Risk Metrics

* Value at Risk (VaR)
* Conditional Value at Risk (CVaR)
* Drawdown Analysis
* Tail Risk Estimation
* Portfolio Risk Metrics

---

## Phase 2.2 — Portfolio Simulation

* Multi-Asset Portfolios
* Correlation Modeling
* Portfolio Monte Carlo Simulation
* Portfolio Optimization

---

## Phase 3 — Synthetic Financial Data Generation

* Variational Autoencoders (VAE)
* TimeGAN
* Diffusion Models
* Synthetic Financial Time Series

---

## Phase 4 — AI Sentiment Engine

* Financial News Ingestion
* FinBERT Sentiment Analysis
* LLM-Based News Understanding
* Synthetic Financial News Generation
* Sentiment-Conditioned Market Simulation

---

## Phase 5 — Scenario & Stress Testing Engine

Examples:

* Interest Rate Hikes
* Interest Rate Cuts
* Recession Scenarios
* Inflation Shocks
* Commodity Price Crashes
* Geopolitical Events
* Earnings Surprises

Users will be able to simulate portfolio behavior under custom macroeconomic and market conditions.

---

## Phase 6 — Interactive Risk Platform

* FastAPI Backend
* React Frontend
* User Portfolio Upload
* Interactive Scenario Builder
* Real-Time Risk Dashboard

---

# Vision

Build an AI-powered financial simulation ecosystem where users can:

* Simulate interest rate changes
* Analyze volatility shocks
* Test portfolio resilience
* Generate synthetic market conditions
* Model sentiment-driven price movements
* Evaluate investment strategies under uncertainty

The ultimate goal is to create a realistic synthetic financial environment where both market data and market narratives can be generated, manipulated, and analyzed for research, education, and risk management purposes.

---

# License

MIT License

