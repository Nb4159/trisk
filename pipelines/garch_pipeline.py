import pandas as pd
from dotenv import load_dotenv
load_dotenv()
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
def main():
    MLFlowTracker.start_run(run_name="GARCH_Model")
    ticker = "AAPL"
    ingestion = YDataIngestion(ticker)
    df=ingestion.fetch_data(start_date="2018-01-01",
        end_date="2025-01-01"
    )
    df=ReturnFeatures.log_returns(df)
    sharpe=SharpeRatio.calculate(returns=df["log_returns"])
    garch=GARCHModel(df["log_returns"])
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