from pathlib import Path
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
    mu=ReturnEstimator.annualized_return(returns)
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
    metrics=SimulationMetrics.summarize(paths)
    logger.info(f"Simulation metrics: {metrics}")
    paths.to_parquet(f"outputs/forecasts/{ticker}_garch_mc.parquet")
    with open(f"outputs/metrics/{ticker}_garch_mc.json", "w") as f:
        json.dump(metrics, f, indent=4)
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
