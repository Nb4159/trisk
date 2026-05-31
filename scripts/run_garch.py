import argparse

from scripts.generate_config import generate_config
from pipelines.garch_pipeline import run_pipeline
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--ticker", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--horizon", default=5, type=int)
    parser.add_argument("--risk_free_rate", default=0.02, type=float)

    args = parser.parse_args()

    config_path = generate_config(
        ticker=args.ticker,
        start=args.start,
        end=args.end,
        horizon=args.horizon,
        risk_free_rate=args.risk_free_rate
    )

    print(f"Generated config: {config_path}")

    run_pipeline(
        config_path=str(config_path)
    )