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
from services.risk_models.risk_report import CalculateRiskMetrics
from services.risk_models.backtesting import VarBacktester
from services.simulation.jump_calibrate import JumpCalibration
from services.simulation.jump_diffusion import JumpDiffusionSimulator
from services.simulation.jump_metrics import JumpMetrics
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
    #Ingestion
    ticker = config["data"]["ticker"]

    logger.info(f"Running simulation for {ticker}")

    MLFlowTracker.start_run(f"{ticker}_garch_mc")
    ingestion=  YDataIngestion(ticker,config["paths"]["raw_data"])
    df=ingestion.fetch_data(start_date=config["date_range"]["start"],
        end_date=config["date_range"]["end"])
    df=ReturnFeatures.log_returns(df)
    returns=df["log_returns"]
    mu=0
    logger.info(f"Annualized return for {ticker}: {mu}")
    #Garch Model Fitting
    garch_model=GARCHModel(returns)
    fitted=garch_model.fit(p=config["garch"]["p"],
        q=config["garch"]["q"])
    
    volatility_forecast=garch_model.forecast_volatility(fitted,horizon=config["simulation"]["horizon_days"])
    logger.info("Generated volatility forecast")
    
    #1. GBM based Monte Carlo Simulation
    simulator=GBMSimulator(initial_price=df["Close"].iloc[-1],mu=mu,volatility_path=volatility_forecast,simulations=config["simulation"]["simulations"])
    paths=simulator.simulate()
    logger.info("Generated GBM simulations")
    final_prices=paths.iloc[-1]
    initialPrice=paths.iloc[0,0]
    simulated_returns=(final_prices - initialPrice) / initialPrice #GBM returns
    # 2. Jump Diffusion based Monte Carlo Simulation
    jump_params = JumpCalibration.calibrate(df["log_returns"])
    MLFlowTracker.log_params("jump_lambda",jump_params["jump_lambda"])
    MLFlowTracker.log_params("jump_mu",jump_params["jump_mu"])
    MLFlowTracker.log_params("jump_sigma",jump_params["jump_sigma"])
    jump_simulator =JumpDiffusionSimulator(
            initial_price=df["Close"].iloc[-1],
            mu=mu,
            volatility_path=volatility_forecast,
            jump_lambda=jump_params["jump_lambda"],
            jump_mu=jump_params["jump_mu"],
            jump_sigma=jump_params["jump_sigma"],
            simulations=config["simulation"]["simulations"]
        )

    jump_paths =jump_simulator.simulate()
    logger.info("Generated Jump Diffusion simulations")
    jump_returns=(jump_paths.iloc[-1] - initialPrice) / initialPrice
    comparison = JumpMetrics.compare_tail_risk(simulated_returns, jump_returns)
    for k, v in comparison.items():
        MLFlowTracker.log_metrics(k,v)
    print("Tail risk comparison between GBM and Jump Diffusion:", comparison)
    
    logger.info("Calculating risk metrics for GBM simulations")
    risk_report_gbm=CalculateRiskMetrics(returns=simulated_returns,initial_price=initialPrice,final_prices=final_prices,paths=paths).generate_report()
    for k, v in risk_report_gbm.items():
        MLFlowTracker.log_metrics(k, v)
    print(risk_report_gbm)
    logger.info("Calculating risk metrics for Jump Diffusion simulations")
    risk_report_jump=CalculateRiskMetrics(returns=jump_returns,initial_price=initialPrice,final_prices=jump_paths.iloc[-1],paths=jump_paths).generate_report()
    for k,v in risk_report_jump.items():
        MLFlowTracker.log_metrics(f"jump_{k}", v)
    print(risk_report_jump)
    window = 252

    var_series = returns.rolling(config["backtesting"]["window"]).apply(
        lambda x: ValueAtRisk.historical(pd.Series(x), confidence=config["backtesting"]["confidence"])
    ).dropna()
    returns_aligned = returns.loc[var_series.index]
    backtest_report =VarBacktester.summary(
            returns=returns_aligned,
            var_series=var_series,
            confidence=config["backtesting"]["confidence"]
        )
    print(backtest_report)
    
    for k, v in backtest_report.items():
        MLFlowTracker.log_metrics(k, v)
    metrics=SimulationMetrics.summarize(paths)
    logger.info(f"Simulation metrics: {metrics}")
    
    paths.to_parquet(f"outputs/forecasts/{ticker}_garch_mc.parquet")
    with open(f"outputs/metrics/{ticker}_garch_mc.json", "w") as f:
        json.dump(metrics, f, indent=4)
    with open(f"outputs/metrics/{ticker}_risk_metrics_gbm.json", "w") as f:
        json.dump(risk_report_gbm, f, indent=4)
    with open(f"outputs/metrics/{ticker}_risk_metrics_jump.json", "w") as f:
        json.dump(risk_report_jump, f, indent=4)
    with open(f"outputs/metrics/{ticker}_backtest_metrics.json", "w") as f:
        json.dump(backtest_report, f, indent=4)
    MonteCarloPlotter.plot(
        paths=paths,
        ticker=ticker,
        save_path=f"outputs/figures/{ticker}_garch_gbm_mc.html"
    ) 
    MonteCarloPlotter.plot(
        paths=jump_paths,
        ticker=ticker,
        save_path=f"outputs/figures/{ticker}_garch_jump_mc.html"
    ) 
    for k, v in metrics.items():
        MLFlowTracker.log_metrics(k, v)
    MLFlowTracker.log_params("ticker", ticker)
    MLFlowTracker.log_params("simulations", config["simulation"]["simulations"])
    MLFlowTracker.end_run()
    logger.info("Pipeline completed")
if __name__ == "__main__":
    main()
