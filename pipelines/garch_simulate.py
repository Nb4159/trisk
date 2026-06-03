from pathlib import Path
import pandas as pd
import numpy as np
import json
import logging
import argparse
from configs.settings import load_config
from services.ingestion.yahoo_finance import YDataIngestion
from models.garch.garch_model import GARCHModel
from services.feature_engineering.returns import ReturnFeatures
from services.simulation.gbm import GBMSimulator
from services.risk_models.return_estimator import ReturnEstimator
from services.tracking.mlflow_tracking import MLFlowTracker
from services.visualization.monte_carlo_plot import MonteCarloPlotter
from services.risk_models.simulation_metrics import SimulationMetrics
from services.risk_models.var import ValueAtRisk
from services.risk_models.cvar import ConditionalVAR
from services.risk_models.probability_metrics import ProbabilityMetrics
from services.risk_models.drawdown import Drawdown 
from services.risk_models.backtesting import VarBacktester

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser()

parser.add_argument(
    "--config",
    required=True,
    help="Path to config YAML"
)

args = parser.parse_args()
config = load_config(args.config)
def main():
    ticker = config["data"]["ticker"]

    logger.info(f"Running simulation for {ticker}")

    MLFlowTracker.start_run(f"{ticker}_garch_mc")
    ingestion=  YDataIngestion(ticker,config["paths"]["raw_data"])
    df=ingestion.fetch_data(start_date=config["date_range"]["start"],
        end_date=config["date_range"]["end"])
    df=ReturnFeatures.log_returns(df)
    returns=df["log_returns"]
    mu=0#ReturnEstimator.annualized_return(returns)
    #print(mu)
    logger.info(f"Annualized return for {ticker}: {mu}")
    garch_model=GARCHModel(returns)
    fitted=garch_model.fit(p=config["garch"]["p"],
        q=config["garch"]["q"])
    
    volatility_forecast=garch_model.forecast_volatility(fitted,horizon=config["simulation"]["horizon_days"])
    logger.info("Generated volatility forecast:")
    simulator=GBMSimulator(initial_price=df["Close"].iloc[-1],mu=mu,volatility_path=volatility_forecast,simulations=config["simulation"]["simulations"])
    paths=simulator.simulate()
    logger.info("Generated GBM simulations")
    final_prices=paths.iloc[-1]
    initialPrice=paths.iloc[0,0]
    simulated_returns=(final_prices - initialPrice) / initialPrice
    var95 = ValueAtRisk.monte_carlo(
    simulated_returns,
        confidence=0.95
    )

    var99 = ValueAtRisk.monte_carlo(
        simulated_returns,
        confidence=0.99
    )   
    cvar95 = (
        ConditionalVAR
        .monte_carlo(
            simulated_returns,
            confidence=0.95
        )
    )

    cvar99 = (
        ConditionalVAR
        .monte_carlo(
            simulated_returns,
            confidence=0.99
        )
    )
    mean_path = paths.mean(axis=1)

    max_dd =max_dd = paths.apply(Drawdown.max_drawdown).mean()
    

    recovery_days =int(paths.apply(Drawdown.recovery_period).mean())
    
    prob_loss = (
        ProbabilityMetrics
        .probability_of_loss(
            final_prices,
            initialPrice
        )
    )

    prob_10_loss = (
        ProbabilityMetrics
        .probability_of_loss_pct(
            final_prices,
            initialPrice,
            0.10
        )
    )

    prob_20_gain = (
        ProbabilityMetrics
        .probability_of_gain_pct(
            final_prices,
            initialPrice,
            0.20
        )
    )
    risk_report = {

        "var_95": float(var95),
        "var_99": float(var99),

        "cvar_95": float(cvar95),
        "cvar_99": float(cvar99),

        "max_drawdown": float(max_dd),
        "recovery_days": int(recovery_days),

        "probability_of_loss":
            float(prob_loss),

        "probability_of_10pct_loss":
            float(prob_10_loss),

        "probability_of_20pct_gain":
            float(prob_20_gain)
    }
    
    for k, v in risk_report.items():
        MLFlowTracker.log_metrics(k, v)
    print(risk_report)
    window = 252

    var_series = returns.rolling(window).apply(
        lambda x: ValueAtRisk.historical(pd.Series(x), confidence=0.95)
    ).dropna()
    returns_aligned = returns.loc[var_series.index]
    backtest_report = (
    VarBacktester.summary(
            returns=returns_aligned,
            var_series=var_series,
            confidence=0.95
        )
    )

    print(backtest_report)
    for k, v in backtest_report.items():
        MLFlowTracker.log_metrics(k, v)
    metrics=SimulationMetrics.summarize(paths)
    logger.info(f"Simulation metrics: {metrics}")
    paths.to_parquet(f"outputs/forecasts/{ticker}_garch_mc.parquet")
    with open(f"outputs/metrics/{ticker}_garch_mc.json", "w") as f:
        json.dump(metrics, f, indent=4)
    with open(f"outputs/metrics/{ticker}_risk_metrics.json", "w") as f:
        json.dump(risk_report, f, indent=4)
    with open(f"outputs/metrics/{ticker}_backtest_metrics.json", "w") as f:
        json.dump(backtest_report, f, indent=4)
    MonteCarloPlotter.plot(
        paths=paths,
        ticker=ticker,
        save_path=f"outputs/figures/{ticker}_garch_mc.html"
    ) 
    for k, v in metrics.items():
        MLFlowTracker.log_metrics(k, v)

    MLFlowTracker.log_params("ticker", ticker)
    MLFlowTracker.log_params("simulations", config["simulation"]["simulations"])

    MLFlowTracker.end_run()
    logger.info("Pipeline completed")
if __name__ == "__main__":
    main()
