# AI-Driven Financial Risk Engine - Complete Flow Documentation

**Generated:** June 1, 2026  
**Status:** Phase 1 ✅ | Phase 2 🚧 (In Progress)

---

## 1. PROJECT ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTRY POINTS                                 │
├─────────────────────────────────────────────────────────────────┤
│ • API Server: /api/main.py                                      │
│ • CLI - GARCH Pipeline: /pipelines/garch_pipeline.py            │
│ • CLI - Simulation: /pipelines/garch_simulate.py                │
│ • Tech Stack: FastAPI, Docker, Python 3.11                      │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│              DATA INGESTION & PROCESSING LAYER                  │
├─────────────────────────────────────────────────────────────────┤
│ • Yahoo Finance API Integration                                 │
│ • DuckDB / Parquet Storage                                      │
│ • Feature Engineering                                           │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│          QUANTITATIVE ANALYSIS & MODELING LAYER                 │
├─────────────────────────────────────────────────────────────────┤
│ • Risk Metrics (Sharpe Ratio, Volatility)                       │
│ • GARCH Volatility Forecasting                                  │
│ • GBM Monte Carlo Simulation                                    │
│ • Validation (Stationarity, ACF/PACF)                           │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│           EXPERIMENT TRACKING & VISUALIZATION                   │
├─────────────────────────────────────────────────────────────────┤
│ • MLflow Tracking (SQLite Backend)                              │
│ • Interactive Plotly Visualizations                             │
│ • Metrics Export (JSON/Parquet)                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. ENTRY POINTS & ENDPOINTS

### 2.1 REST API Endpoints
**File:** `api/main.py`  
**Framework:** FastAPI v0.1.0  

| Endpoint | Method | Status | Function | Response |
|----------|--------|--------|----------|----------|
| `/` | GET | ✅ | `root()` | `{"message": "Risk Engine Running"}` |
| **Future Endpoints** |
| `/analyze/{ticker}` | POST | 🚧 | GARCH Analysis | Risk metrics JSON |
| `/forecast/{ticker}` | GET | 🚧 | Volatility Forecast | Forecast data |
| `/simulate/{ticker}` | POST | 🚧 | Monte Carlo | Simulation results |

**Launch Command:**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 2.2 CLI Pipelines

#### **Pipeline A: GARCH Risk Analysis**
**File:** `pipelines/garch_pipeline.py`

**Entry Point:** `main()`  
**Config Input:** YAML configuration file (via `--config` argument)

```bash
python pipelines/garch_pipeline.py --config configs/base.yaml
```

**Execution Flow:**
```
1. MLFlowTracker.start_run("GARCH_Model")
2. YDataIngestion.fetch_data()
3. ReturnFeatures.log_returns()
4. ReturnFeatures.rolling_volatility()
5. StationarityTest.adf_test()
6. SharpeRatio.calculate()
7. GARCHModel.fit()
8. GARCHModel.forecast_volatility()
9. ACF_PACF.generate()
10. Visualization.plot()
11. MLFlowTracker.end_run()
```

#### **Pipeline B: Monte Carlo Simulation**
**File:** `pipelines/garch_simulate.py`

**Entry Point:** `main()`  
**Config Input:** YAML configuration file (via `--config` argument)

```bash
python pipelines/garch_simulate.py --config configs/base.yaml
```

**Execution Flow:**
```
1. MLFlowTracker.start_run(f"{ticker}_garch_mc")
2. YDataIngestion.fetch_data()
3. ReturnFeatures.log_returns()
4. ReturnEstimator.annualized_return()
5. GARCHModel.fit()
6. GARCHModel.forecast_volatility()
7. GBMSimulator.simulate()
8. SimulationMetrics.summarize()
9. Export to Parquet & JSON
10. MonteCarloPlotter.plot()
11. MLFlowTracker.log_metrics() & log_params()
12. MLFlowTracker.end_run()
```

---

## 3. COMPLETE DATA FLOW DIAGRAM

```
EXTERNAL DATA SOURCES
        ↓
┌──────────────────────────────────────────────────────────────────┐
│ INGESTION LAYER                                                  │
│ • YDataIngestion.fetch_data(ticker, start_date, end_date)        │
│   └─ Input: Ticker (str), Date Range                             │
│   └─ Output: DataFrame [Close, Open, High, Low, Volume]          │
│   └─ Storage: Parquet files @ data/raw/{ticker}.parquet          │
└──────────────────────────────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────────────────────────┐
│ FEATURE ENGINEERING LAYER                                        │
│ • ReturnFeatures.log_returns(df)                                 │
│   └─ Input: DataFrame with 'Close' column                        │
│   └─ Output: DataFrame + 'log_returns' column                    │
│   └─ Formula: log(Close_t / Close_t-1)                           │
│                                                                  │
│ • ReturnFeatures.rolling_volatility(df, window=21)               │
│   └─ Input: DataFrame with 'log_returns'                         │
│   └─ Output: DataFrame + 'rolling_volatility' column             │
│   └─ Formula: std(returns) * sqrt(252), annualized               │
└──────────────────────────────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────────────────────────┐
│ VALIDATION LAYER                                                 │
│ • StationarityTest.adf_test(series)                              │
│   └─ Input: Series of returns                                    │
│   └─ Output: {adf_statistic, p_value, critical_values}           │
│   └─ Condition: p-value < 0.05 = Stationary                     │
│                                                                  │
│ • ACF_PACF.generate(series, lags=50)                             │
│   └─ Input: Series of squared returns                            │
│   └─ Output: PNG plot @ outputs/figures/acf_pacf.png             │
└──────────────────────────────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────────────────────────┐
│ RISK METRICS LAYER                                               │
│ • SharpeRatio.calculate(returns, risk_free_rate=0.02)            │
│   └─ Input: Series of returns, risk-free rate (annual)           │
│   └─ Output: Sharpe ratio (float)                                │
│   └─ Formula: (mean_excess_returns / std) * sqrt(252)            │
│                                                                  │
│ • ReturnEstimator.annualized_return(returns)                     │
│   └─ Input: Series of daily returns                              │
│   └─ Output: Annualized return (float)                           │
│   └─ Formula: mean(returns) * 252                                │
└──────────────────────────────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────────────────────────┐
│ GARCH MODELING LAYER                                             │
│ • GARCHModel.fit(returns, p, q)                                  │
│   └─ Input: Series of returns, GARCH order (p, q)               │
│   └─ Output: Fitted ARCH model object                            │
│   └─ Config: dist="t", vol="Garch"                               │
│                                                                  │
│ • GARCHModel.forecast_volatility(model, horizon=252)             │
│   └─ Input: Fitted model, forecast horizon (days)                │
│   └─ Output: Array of volatility forecasts                       │
│   └─ Formula: sqrt(forecasted_variances)                         │
└──────────────────────────────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────────────────────────┐
│ SIMULATION LAYER (Monte Carlo)                                   │
│ • GBMSimulator.simulate()                                        │
│   └─ Input: initial_price, mu, volatility_path, simulations      │
│   └─ Output: DataFrame [horizon+1 rows × simulations columns]    │
│   └─ Formula: dS = mu*S*dt + sigma*S*dW (Geometric Brownian)    │
│   └─ Config: dt = 1/252, seed = 42, antithetic reduction         │
│                                                                  │
│ • SimulationMetrics.summarize(paths)                             │
│   └─ Input: DataFrame of simulated price paths                   │
│   └─ Output: {                                                   │
│       mean_price, median_price, min_price, max_price,            │
│       p01, p05, p95, p99                                         │
│     }                                                            │
└──────────────────────────────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────────────────────────┐
│ EXPORT & PERSISTENCE LAYER                                      │
│ • Parquet: outputs/forecasts/{ticker}_garch_mc.parquet           │
│ • JSON Metrics: outputs/metrics/{ticker}_garch_mc.json           │
│ • SQLite MLflow: mlruns.db                                       │
└──────────────────────────────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────────────────────────┐
│ VISUALIZATION & TRACKING LAYER                                   │
│ • PricePlot.plot(df, ticker)                                     │
│   └─ Output: {ticker}_price_plot.html                            │
│   └─ Library: Plotly                                             │
│                                                                  │
│ • RollingVolatilityPlot.plot(df, ticker)                         │
│   └─ Output: {ticker}_rolling_volatility.html                    │
│   └─ Library: Plotly                                             │
│                                                                  │
│ • GARCHForecastPlot.plot(forecasted_vol, ticker)                 │
│   └─ Output: {ticker}_garch_forecast_plot.html                   │
│   └─ Library: Plotly                                             │
│                                                                  │
│ • MonteCarloPlotter.plot(paths, ticker)                          │
│   └─ Output: {ticker}_garch_mc.html (100 sample paths)           │
│   └─ Library: Plotly                                             │
│                                                                  │
│ • MLFlowTracker                                                  │
│   ├─ start_run(run_name)                                         │
│   ├─ log_params(key, value)                                      │
│   ├─ log_metrics(key, value)                                     │
│   └─ end_run()                                                   │
│   └─ Tracking URI: sqlite:///mlruns.db                           │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. SERVICE MODULES REFERENCE

### 4.1 Ingestion Services
**Module:** `services/ingestion/yahoo_finance.py`

```
Class: YDataIngestion
├─ __init__(ticker: str, data_dir: str)
│  └─ Creates/validates data directory
│
├─ fetch_data(start_date, end_date) → DataFrame
│  └─ Input: Date strings (YYYY-MM-DD format)
│  └─ Output: OHLCV DataFrame with NaN values dropped
│  └─ Uses: yfinance.download()
│  └─ Auto-adjustment: True
│
├─ save_parquet(df) → None
│  └─ Writes DataFrame to: data/raw/{ticker}.parquet
│
└─ load_parquet() → DataFrame
   └─ Reads from: data/raw/{ticker}.parquet
```

---

### 4.2 Feature Engineering Services
**Module:** `services/feature_engineering/returns.py`

```
Class: ReturnFeatures (static methods)
├─ log_returns(df: DataFrame) → DataFrame
│  └─ Adds 'log_returns' column
│  └─ Formula: np.log(Close / Close.shift(1))
│  └─ Drops NaN values
│
└─ rolling_volatility(df: DataFrame, window: int = 21) → DataFrame
   └─ Adds 'rolling_volatility' column
   └─ Formula: std(log_returns).rolling(window) * sqrt(252)
   └─ Annualized volatility
```

---

### 4.3 Risk Model Services
**Module:** `services/risk_models/`

#### **Sharpe Ratio Calculation**
```python
# File: sharpe.py
Class: SharpeRatio
└─ calculate(returns, risk_free_rate=0.02) → float
   └─ Input: Daily returns series, annual risk-free rate
   └─ Formula: (mean(excess_returns) / std(excess_returns)) * sqrt(252)
   └─ excess_returns = returns - (rf/252)
```

#### **Return Estimator**
```python
# File: return_estimator.py
Class: ReturnEstimator
└─ annualized_return(returns) → float
   └─ Formula: mean(returns) * 252
```

#### **Simulation Metrics**
```python
# File: simulation_metrics.py
Class: SimulationMetrics
└─ summarize(paths: DataFrame) → dict
   └─ Returns: {
       "mean_price": float,
       "median_price": float,
       "min_price": float,
       "max_price": float,
       "p01": float (1st percentile),
       "p05": float (5th percentile),
       "p95": float (95th percentile),
       "p99": float (99th percentile)
     }
```

---

### 4.4 Validation Services
**Module:** `services/validation/`

#### **Stationarity Test (ADF)**
```python
# File: stationarity.py
Class: StationarityTest
└─ adf_test(series) → dict
   └─ Returns: {
       'adf_statistic': float,
       'p-value': float,
       'critical_values': dict
     }
   └─ Interpretation: p-value < 0.05 ⟹ Stationary
```

#### **ACF/PACF Analysis**
```python
# File: order_determine.py
Class: ACF_PACF
└─ generate(series, lags=50, save_path) → PNG file
   └─ Plots ACF and PACF side-by-side
   └─ Used to determine GARCH order
```

---

### 4.5 Simulation Services
**Module:** `services/simulation/gbm.py`

```python
Class: GBMSimulator
├─ __init__(initial_price, mu, volatility_path, simulations)
│  └─ initial_price: Current stock price (float)
│  └─ mu: Annualized drift (float)
│  └─ volatility_path: Array of daily volatilities
│  └─ simulations: Number of paths (int)
│
└─ simulate() → DataFrame
   └─ Returns: DataFrame[horizon+1 × simulations]
   └─ Implementation:
      - dt = 1/252
      - Uses antithetic variance reduction
      - Seed = 42 (reproducible)
      - Formula: dS = mu*S*dt + sigma*S*dW
```

---

### 4.6 Visualization Services
**Module:** `services/visualization/`

| Class | Function | Output |
|-------|----------|--------|
| `PricePlot` | `plot(df, ticker, save_path)` | `{ticker}_price_plot.html` |
| `RollingVolatilityPlot` | `plot(df, ticker, plot_path)` | `{ticker}_rolling_volatility.html` |
| `GARCHForecastPlot` | `plot(forecasted_vol, ticker, save_path)` | `{ticker}_garch_forecast_plot.html` |
| `MonteCarloPlotter` | `plot(paths, ticker, save_path)` | `{ticker}_garch_mc.html` |

**Library:** Plotly (Interactive HTML)

---

### 4.7 Tracking Services
**Module:** `services/tracking/mlflow_tracking.py`

```python
Class: MLFlowTracker
├─ start_run(run_name: str) → None
│  └─ Initializes MLflow run
│
├─ log_params(key: str, value) → None
│  └─ Logs hyperparameters
│
├─ log_metrics(key: str, value: float) → None
│  └─ Logs numeric metrics
│
└─ end_run() → None
   └─ Closes current run

Configuration:
  Tracking URI: sqlite:///mlruns.db
  Backend: SQLite
```

---

### 4.8 Database Services
**Module:** `services/database/duckdb_client.py`

```python
Class: DuckClient
├─ __init__(db_path: str = "riskengine.duckdb")
│
├─ create_table() → None
│  └─ Creates: prices(Date, Open, High, Low, Close, Volume)
│
├─ insert_data(df: DataFrame) → None
│  └─ Batch inserts from DataFrame
│
└─ query(sql: str) → DataFrame
   └─ Executes SQL and returns results
```

---

## 5. GARCH MODEL IMPLEMENTATION

**Module:** `models/garch/garch_model.py`

```python
Class: GARCHModel
├─ __init__(returns: pd.Series)
│  └─ Scales returns: returns * 100
│
├─ fit(p: int, q: int) → arch.ARCHModelResult
│  └─ Model: GARCH(p, q) with t-distribution
│  └─ Specification:
│     - vol: "Garch"
│     - p: AR order (default 1)
│     - q: MA order (default 1)
│     - dist: "t" (Student's t-distribution)
│  └─ Returns: Fitted model object
│
└─ forecast_volatility(model, horizon: int = 252) → np.array
   └─ Input: Fitted model, forecast horizon
   └─ Output: Volatility forecasts (in %)
   └─ Calculation: sqrt(forecasted_variances)
```

**Library:** `arch` (Autoregressive Conditional Heteroskedasticity)

---

## 6. CONFIGURATION SYSTEM

**File:** `configs/settings.py` / `configs/base.yaml`

```yaml
project:
  name: risk-engine

data:
  ticker: HDFCBANK.NS  # Configurable ticker

date_range:
  start: "2024-01-01"
  end: "2026-01-01"

risk:
  risk_free_rate: 0.02      # 2% annual
  realized_vol_window: 21   # Business days

garch:
  p: 1                      # AR order
  q: 1                      # MA order

paths:
  raw_data: data/raw
  processed_data: data/processed
  outputs: outputs

simulation:
  horizon_days: 120         # Forecast period
  simulations: 5000         # Monte Carlo paths
```

**Loading Function:**
```python
def load_config(config_path: str) → dict
  └─ Parses YAML configuration
  └─ Returns: Configuration dictionary
```

---

## 7. OUTPUT DIRECTORY STRUCTURE

```
outputs/
├── figures/
│   ├── {ticker}_price_plot.html           [Interactive price chart]
│   ├── {ticker}_rolling_volatility.html    [Volatility over time]
│   ├── {ticker}_garch_forecast_plot.html   [Forecasted volatility]
│   ├── {ticker}_garch_mc.html              [Monte Carlo paths]
│   └── acf_pacf.png                        [ACF/PACF diagnostics]
├── forecasts/
│   └── {ticker}_garch_mc.parquet           [Simulated price paths]
└── metrics/
    └── {ticker}_garch_mc.json              [Summary statistics]

data/
├── raw/
│   └── {ticker}.parquet                    [Historical OHLCV data]
├── processed/                              [Future use]
└── synthetic/                              [Future use]
```

---

## 8. EXAMPLE EXECUTION TRACE

### Scenario: Analyze TSLA stock with GARCH

**Command:**
```bash
python pipelines/garch_pipeline.py --config configs/base.yaml
```

**Execution Sequence:**

```
1. Load Config
   Input: configs/base.yaml
   Output: config = {ticker: "TSLA", garch: {p: 1, q: 1}, ...}

2. MLflow Session Start
   Run Name: "GARCH_Model"
   Tracking: mlruns.db

3. Data Ingestion
   Function: YDataIngestion.fetch_data()
   Params: ticker="TSLA", start="2024-01-01", end="2026-01-01"
   Output: DataFrame (shape: 500 rows × 6 columns)
   Saved: data/raw/TSLA.parquet

4. Return Calculation
   Function: ReturnFeatures.log_returns()
   Input: Close column
   Output: log_returns column added

5. Rolling Volatility
   Function: ReturnFeatures.rolling_volatility(window=21)
   Output: rolling_volatility column added

6. Validation Tests
   a) Stationarity: ADF test
      Result: p-value = 0.0001 ✓ Stationary
   
   b) Order Detection: ACF/PACF
      Output: acf_pacf.png

7. Risk Metrics
   a) Sharpe Ratio: 0.7882
      Calculation: (mean_excess_returns / std) * sqrt(252)
   
   b) MLflow Logged:
      Metric: sharpe_ratio = 0.7882

8. GARCH Fitting
   Order: (1, 1)
   Distribution: Student's t
   Output: Fitted model object

9. Volatility Forecasting
   Horizon: 252 days
   Output: [1.906, 1.977, 2.045, ..., 2.174] (%)

10. Visualization
    a) Price Plot → outputs/figures/TSLA_price_plot.html
    b) Rolling Vol → outputs/figures/TSLA_rolling_volatility.html
    c) GARCH Forecast → outputs/figures/TSLA_garch_forecast_plot.html

11. MLflow Session End
    Artifacts: Saved to mlruns.db

Output Summary:
✓ 3 HTML visualizations
✓ 1 Parquet data file
✓ MLflow metrics logged
✓ ACF/PACF diagnostics
```

---

## 9. MONTE CARLO SIMULATION EXECUTION

**Command:**
```bash
python pipelines/garch_simulate.py --config configs/base.yaml
```

**Execution Sequence:**

```
1. Load Config & Start MLflow
   Run: "TSLA_garch_mc"

2. Fetch & Process Data
   Functions: YDataIngestion + ReturnFeatures
   Output: log_returns calculated

3. Estimate Parameters
   Annualized Return (mu):
   Formula: mean(returns) * 252
   Result: mu = 0.15 (15% annualized)

4. GARCH Volatility Forecast
   Fitted Model: GARCH(1,1)
   Horizon: 120 days
   Output: [2.1, 2.15, 2.2, ..., 2.3] (%)

5. GBM Simulation
   Class: GBMSimulator
   Params:
     - S0 = 182.45 (current price)
     - μ = 0.15 (annualized drift)
     - σ_t = forecasted volatilities
     - paths = 5000
   
   Process:
     - Generate 5000 correlated paths
     - Time steps: 121 (0 to 120 days)
     - Variance reduction: Antithetic
     - Output: DataFrame(121 × 5000)

6. Summary Statistics
   Final prices from all paths:
   {
     "mean_price": 185.32,
     "median_price": 184.91,
     "min_price": 142.55,
     "max_price": 241.83,
     "p01": 151.23,  (1% chance price ≤ this)
     "p05": 160.45,  (5% chance price ≤ this)
     "p95": 210.67,  (95% chance price ≤ this)
     "p99": 228.34   (99% chance price ≤ this)
   }

7. Export Results
   a) Parquet: outputs/forecasts/TSLA_garch_mc.parquet
   b) JSON: outputs/metrics/TSLA_garch_mc.json
   c) MLflow metrics logged

8. Visualization
   Function: MonteCarloPlotter.plot()
   - Plots first 100 of 5000 paths
   - Interactive Plotly chart
   - Output: outputs/figures/TSLA_garch_mc.html

9. MLflow Session End
```

---

## 10. TECHNICAL SPECIFICATIONS

### Dependencies
```
FastAPI >= 0.104.0
yfinance >= 0.2.32
arch >= 5.3.0
numpy >= 1.24.0
pandas >= 2.0.0
plotly >= 5.17.0
statsmodels >= 0.14.0
mlflow >= 2.9.0
duckdb >= 0.9.0
PyYAML >= 6.0
```

### Docker Configuration
```dockerfile
Python 3.11
Environment: Linux
Database: SQLite (MLflow tracking)
Storage: Parquet format for time series data
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | str | HDFCBANK.NS | Stock ticker symbol |
| `start_date` | str | 2024-01-01 | Historical data start |
| `end_date` | str | 2026-01-01 | Historical data end |
| `risk_free_rate` | float | 0.02 | Annual risk-free rate |
| `window` | int | 21 | Rolling volatility window |
| `p` | int | 1 | GARCH AR order |
| `q` | int | 1 | GARCH MA order |
| `horizon_days` | int | 120 | Forecast horizon |
| `simulations` | int | 5000 | Monte Carlo paths |

---

## 11. DATA TYPES & FORMATS

### Input Data Types
- **Ticker:** String (e.g., "TSLA", "AAPL", "HDFCBANK.NS")
- **Dates:** String in format "YYYY-MM-DD"
- **Returns:** Float, daily decimal returns
- **Prices:** Float, USD or local currency

### Output Data Types
- **Metrics:** JSON (dictionaries with float values)
- **Forecasts:** Parquet (columnar format for efficiency)
- **Visualizations:** HTML (interactive Plotly)
- **Diagnostics:** PNG (matplotlib)

---

## 12. ERROR HANDLING & VALIDATION

### Validation Points
1. **Data Validation:** Missing data (NaN) dropped automatically
2. **Stationarity Test:** ADF p-value < 0.05 required
3. **GARCH Fit:** Convergence verified by `arch` library
4. **Simulation:** Antithetic reduction for variance reduction

### Logging
- **Level:** INFO
- **Format:** Console output
- **Tracking:** MLflow runs stored in SQLite

---

## 13. CURRENT STATUS & ROADMAP

### ✅ Phase 1 Complete
- [x] Historical data ingestion (Yahoo Finance)
- [x] Feature engineering (returns, volatility)
- [x] GARCH volatility forecasting
- [x] Risk metrics (Sharpe ratio)
- [x] Validation tests (ADF, ACF/PACF)
- [x] Interactive visualizations (Plotly)
- [x] Experiment tracking (MLflow)
- [x] Docker containerization
- [x] Config-driven execution

### 🚧 Phase 2 In Progress
- [x] GBM simulation implementation
- [x] Monte Carlo price path generation
- [ ] Value at Risk (VaR)
- [ ] Conditional Value at Risk (CVaR)
- [ ] Drawdown analysis
- [ ] Probability of loss metrics
- [ ] Portfolio-level simulations

### 🔮 Phase 3 Planned
- [ ] VAE synthetic data generation
- [ ] GAN market simulation
- [ ] Diffusion models
- [ ] LLM sentiment analysis
- [ ] Advanced portfolio optimization
- [ ] Scenario analysis framework

---

## 14. SUMMARY TABLE: FUNCTIONS & RETURNS

| Function | Module | Input | Output | Use Case |
|----------|--------|-------|--------|----------|
| `YDataIngestion.fetch_data()` | ingestion | Ticker, dates | DataFrame | Get historical data |
| `ReturnFeatures.log_returns()` | feature_eng | DataFrame | DataFrame + log_returns | Calculate daily returns |
| `ReturnFeatures.rolling_volatility()` | feature_eng | DataFrame, window | DataFrame + rolling_vol | Estimate realized volatility |
| `SharpeRatio.calculate()` | risk_models | Returns, rf_rate | float | Risk-adjusted return metric |
| `ReturnEstimator.annualized_return()` | risk_models | Returns | float | Expected annual return |
| `GARCHModel.fit()` | models/garch | Returns, p, q | Fitted model | Fit volatility model |
| `GARCHModel.forecast_volatility()` | models/garch | Model, horizon | np.array | Predict future volatility |
| `GBMSimulator.simulate()` | simulation | S0, μ, σ, N | DataFrame | Generate price paths |
| `SimulationMetrics.summarize()` | risk_models | Paths | dict | Calculate statistics |
| `StationarityTest.adf_test()` | validation | Series | dict | Test data stationarity |
| `ACF_PACF.generate()` | validation | Series, lags | PNG file | Diagnostic plots |
| `PricePlot.plot()` | visualization | DataFrame, ticker | HTML file | Price chart |
| `MonteCarloPlotter.plot()` | visualization | Paths, ticker | HTML file | Simulation visualization |
| `MLFlowTracker.log_metrics()` | tracking | Key, value | None | Log experiment metrics |

---

## 15. CONTACT & DOCUMENTATION

- **Project:** AI-Driven Financial Risk Engine
- **Version:** 0.1.0
- **Phase:** 1 ✅ | 2 🚧
- **Tech Stack:** Python 3.11 | FastAPI | Docker
- **Data:** Yahoo Finance | DuckDB | Parquet
- **Models:** GARCH | GBM | Monte Carlo
- **Tracking:** MLflow + SQLite

---

**Report Generated:** June 1, 2026
