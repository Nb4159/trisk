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
from services.validation.stationarity import (
    StationarityTest
)
from services.validation.order_determine import (
    ACF_PACF
)
from services.visualization.price_plot import (
    PricePlot
)
from services.visualization.rolling_volatility import (
    RollingVolatilityPlot
)
from services.visualization.garch_forecast_plot import (
    GARCHForecastPlot
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
    ingestion.save_parquet(df)
    df=ReturnFeatures.log_returns(df)
    df = ReturnFeatures.rolling_volatility(
    df,
    window=21#config["risk"]["vol_window"]
    )
    stationarity_result=StationarityTest.adf_test(df["log_returns"])
    print("Stationarity Test Result (p-value < 0.05=> Stationary):", stationarity_result)
    sharpe=SharpeRatio.calculate(returns=df["log_returns"],risk_free_rate=config["risk"]["risk_free_rate"])
    garch=GARCHModel(df["log_returns"])
    fitted_model=garch.fit(p=config["garch"]["p"],
                            q=config["garch"]["q"])
    forecasted_volatility=garch.forecast_volatility(fitted_model,horizon=config["garch"]["horizon"])
    print(f"Sharpe Ratio: {sharpe}")
    print(f"Forecasted Volatility: {forecasted_volatility}")
    MLFlowTracker.log_metrics(
        "sharpe_ratio", sharpe
        #"forecasted_volatility": forecasted_volatility
    )
    
    ACF_PACF.generate(df["log_returns"]**2)
    PricePlot.plot(df, ticker, save_path=f"outputs/figures/{ticker}_price_plot.html")
    #df = ReturnFeatures.rolling_volatility(df)
    RollingVolatilityPlot.plot(df, ticker, plot_path=f"outputs/figures/{ticker}_rolling_volatility.html")
    GARCHForecastPlot.plot(forecasted_volatility, ticker, save_path=f"outputs/figures/{ticker}_garch_forecast_plot.html")
    MLFlowTracker.end_run()
if __name__ == "__main__":
    main()