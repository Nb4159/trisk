import pandas as pd
import numpy as np
class ReturnFeatures:
    @staticmethod
    def log_returns(df):
        df["log_returns"]=np.log(df["Close"]/df["Close"].shift(1))
        return df.dropna()
    @staticmethod
    def rolling_volatility(
        df: pd.DataFrame,
        window: int = 21
    ) -> pd.DataFrame:

        df["rolling_volatility"] = (
            df["log_returns"]
            .rolling(window)
            .std()
            * np.sqrt(252)
        )

        return df 