from abc import ABC, abstractmethod
import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD
class BaseIndicatorHandler(ABC):
    
    @abstractmethod
    def compute(self, df):
        """Compute indicator and add columns to df inplace."""
        pass

    @abstractmethod
    def plot(self, ax, df):
        """Plot indicator on the given matplotlib axis."""
        pass

    def is_computed(self, df, *columns):
        """Helper to check if indicator columns already exist in df."""
        return all(col in df.columns for col in columns)
class RSIIndicatorHandler(BaseIndicatorHandler):
    def compute(self, df):
        if not self.is_computed(df, "rsi"):
            df["rsi"] = RSIIndicator(df["Close"]).rsi()

    def plot(self, ax, df):
        ax.plot(df.index, df["rsi"], color="purple", label="RSI")
        ax.axhline(70, color="red", linestyle="--", linewidth=0.8)
        ax.axhline(30, color="green", linestyle="--", linewidth=0.8)
        ax.set_title("RSI")
        ax.legend()
        ax.grid(True)


class MACDIndicatorHandler(BaseIndicatorHandler):
    def compute(self, df):
        if not self.is_computed(df, "macd", "macd_signal"):
            macd = MACD(df["Close"])
            df["macd"] = macd.macd()
            df["macd_signal"] = macd.macd_signal()

    def plot(self, ax, df):
        ax.plot(df.index, df["macd"], label="MACD", color="blue")
        ax.plot(df.index, df["macd_signal"], label="Signal", color="orange")
        ax.bar(df.index, df["macd"] - df["macd_signal"], color="gray", alpha=0.4, label="Histogram")
        ax.set_title("MACD")
        ax.legend()
        ax.grid(True)


class StochIndicatorHandler(BaseIndicatorHandler):
    def compute(self, df):
        if not self.is_computed(df, "stoch_k", "stoch_d"):
            stoch = StochasticOscillator(df["High"], df["Low"], df["Close"])
            df["stoch_k"] = stoch.stoch()
            df["stoch_d"] = stoch.stoch_signal()

    def plot(self, ax, df):
        ax.plot(df.index, df["stoch_k"], label="%K", color="blue")
        ax.plot(df.index, df["stoch_d"], label="%D", color="orange")
        ax.axhline(80, color="red", linestyle="--", linewidth=0.8)
        ax.axhline(20, color="green", linestyle="--", linewidth=0.8)
        ax.set_title("Stochastic Oscillator")
        ax.legend()
        ax.grid(True)