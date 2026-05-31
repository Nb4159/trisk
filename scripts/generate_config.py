import argparse
import yaml

from pathlib import Path
from datetime import datetime

from services.ingestion.yahoo_finance import (
    YDataIngestion
)

from services.feature_engineering.returns import (
    ReturnFeatures
)

"""from services.risk_models.model_selection import (
    find_best_garch_order
)

from services.macro.risk_free_rate import (
    get_risk_free_rate
)"""
def generate_config(
    ticker,
    start,
    end,
    horizon,
    risk_free_rate
):

    ingestion = YDataIngestion(
        ticker=ticker,
        data_dir="data/raw"
    )

    df = ingestion.fetch_data(
        start_date=start,
        end_date=end
    )

    df = ReturnFeatures.log_returns(df)

    p, q = 1,1#find_best_garch_order(
    #    df["log_return"]
    #)

    rf_rate = risk_free_rate# get_risk_free_rate()

    config = {
        "project": {
            "name": "risk-engine"
        },

        "data": {
            "ticker": ticker
        },

        "date_range": {
            "start": start,
            "end": end
        },

        "risk": {
            "risk_free_rate": rf_rate
        },

        "garch": {
            "p": p,
            "q": q,
            "horizon": horizon
        },
        "paths": {
        "raw_data": "data/raw",
        "processed_data": "data/processed",
        "synthetic_data": "data/synthetic",
        "figures": "outputs/figures",
        "forecasts": "outputs/forecasts",
        "metrics": "outputs/metrics"
        },

        "metadata": {
            "generated_at":
                datetime.utcnow().isoformat()
        }
    }

    output_dir = Path(
        "configs/generated"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"{ticker}_"
        f"{datetime.now():%Y%m%d}.yaml"
    )

    output_path = output_dir / filename

    with open(output_path, "w") as file:
        yaml.dump(
            config,
            file,
            sort_keys=False
        )

    """print(
        f"Config saved to: {output_path}"
    )"""
    return output_path
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--ticker",
        required=True
    )

    parser.add_argument(
        "--start",
        required=True
    )

    parser.add_argument(
        "--end",
        required=True
    )

    parser.add_argument(
        "--horizon",
        default=5,
        type=int
    )
    
    parser.add_argument("--risk_free_rate", default=0.02, type=float)

    args = parser.parse_args()

    generate_config(
        ticker=args.ticker,
        start=args.start,
        end=args.end,
        horizon=args.horizon,
        risk_free_rate=args.risk_free_rate
    )