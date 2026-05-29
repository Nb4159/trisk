import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import argparse

from configs.settings import load_config
from services.ingestion.yahoo_finance import (
    YDataIngestion
)

from services.feature_engineering.returns import (
    ReturnFeatures
)

from services.risk_models.sharpe import (
    SharpeRatio
)

from models.garch.garch_model import (
    GARCHModel
)

from services.tracking.mlflow_tracking import (
    MLFlowTracker
)
parser = argparse.ArgumentParser()

parser.add_argument(
    "--config",
    required=True,
    help="Path to config YAML"
)

args = parser.parse_args()
config = load_config(args.config)
def main():
    MLFlowTracker.start_run(run_name="GARCH_Model")
    ticker = config["data"]["ticker"]
    ingestion = YDataIngestion(ticker, config["paths"]["raw_data"])
    df=ingestion.fetch_data(start_date=config["date_range"]["start"],
        end_date=config["date_range"]["end"])

    df=ReturnFeatures.log_returns(df)
    sharpe=SharpeRatio.calculate(returns=df["log_returns"],risk_free_rate=config["risk"]["risk_free_rate"])
    garch=GARCHModel(df["log_returns"],p=config["garch"]["p"],
q=config["garch"]["q"],horizon=config["garch"]["horizon"])
    fitted_model=garch.fit()
    forecasted_volatility=garch.forecast_volatility(fitted_model)
    print(f"Sharpe Ratio: {sharpe}")
    print(f"Forecasted Volatility: {forecasted_volatility}")
    MLFlowTracker.log_metrics(
        "sharpe_ratio", sharpe
        #"forecasted_volatility": forecasted_volatility
    )
    MLFlowTracker.end_run()
if __name__ == "__main__":
    main()