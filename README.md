# AI-Driven Financial Risk Engine

A modular quantitative finance and synthetic market simulation platform focused on:

* volatility forecasting
* portfolio risk analysis
* synthetic financial data generation
* scenario-based market simulations
* AI-driven sentiment modeling

This project combines traditional quantitative finance techniques such as GARCH models and Monte Carlo simulations with modern generative AI approaches including VAEs, GANs, diffusion models, and LLM-based financial sentiment systems.

The long-term goal is to build a realistic financial simulation environment capable of modeling how macroeconomic events, geopolitical shocks, and sentiment changes affect market behavior.

---

# Current Features

## Phase 1 (Completed)

* Financial data ingestion using Yahoo Finance
* Log return calculation
* Rolling volatility estimation
* Sharpe ratio computation
* GARCH volatility forecasting
* DuckDB analytical layer
* Parquet-based storage
* MLflow experiment tracking
* Dockerized development setup

---

# Example Output

```text
Sharpe Ratio: 0.7882748057356007

Forecasted Volatility:
[1.90613251 1.97717036 2.04536768 2.11083806 2.17369054]
```

---

# Tech Stack

* Python
* FastAPI
* DuckDB
* SQLite
* Parquet
* PyTorch
* MLflow
* Weights & Biases
* Docker

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Nb4159/trisk.git
cd risk-engine
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv fna
fna\Scripts\activate
```

### Linux/macOS

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

## Run GARCH Pipeline

```bash
python pipelines/garch_pipeline.py
```

---

## Run MLflow

```bash
mlflow ui --host 0.0.0.0 --port 5000
```

Open in browser:

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

## Phase 2

* Monte Carlo simulation
* Geometric Brownian Motion
* Jump diffusion models
* Portfolio risk simulation

## Phase 3

* VAE-based synthetic data generation
* TimeGAN
* Diffusion models for financial time series

## Phase 4

* LLM-driven financial news generation
* Sentiment-conditioned market simulation
* Scenario-based stress testing

## Phase 5

* Interactive portfolio simulation platform
* Web dashboard
* Multi-agent synthetic market ecosystem

---

# Vision

Build an AI-powered financial simulation system where users can:

* simulate interest rate changes
* analyze volatility shocks
* test portfolio resilience
* generate synthetic market conditions
* evaluate investment strategies under uncertainty

---

# License

MIT License
