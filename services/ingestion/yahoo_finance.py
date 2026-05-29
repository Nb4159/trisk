import yfinance as yf
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)
class YDataIngestion:
    def __init__(self,ticker=str):
        self.ticker = ticker
    def fetch_data(self,start_date,end_date):
        data = yf.download(self.ticker, start=start_date, end=end_date,auto_adjust=True)
        data.dropna(inplace=True)
        return data
    def save_paraquet(self,df):
        file_path=DATA_DIR/f"{self.ticker}.parquet"
        df.to_parquet(file_path)
    def load_paraquet(self):
        file_path=DATA_DIR/f"{self.ticker}.parquet"
        return pd.read_parquet(file_path)
if __name__ == "__main__":
    ingestion=YDataIngestion("AAPL")
    df = ingestion.fetch(
        start="2018-01-01",
        end="2025-01-01"
    )

    ingestion.save_parquet(df)

    print(df.head())