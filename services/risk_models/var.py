import pandas as pd
import numpy as np
from scipy.stats import norm

class ValueAtRisk:
    @staticmethod
    def historical(returns,confidence=0.95):
        return -np.percentile(returns.dropna(),(1-confidence)*100)
    @staticmethod
    def parametric(returns,confidence=0.95):
        mu = returns.mean()
        sigma = returns.std()
        return -norm.ppf(1-confidence)*sigma+mu
    @staticmethod
    def monte_carlo(simulated_returns,confidence=0.95):
        return -np.percentile(simulated_returns.dropna(),(1-confidence)*100)
    @staticmethod
    def dollar_var(returns, portfolio_value, confidence=0.95):
        var_pct = ValueAtRisk.historical(returns, confidence)
        return var_pct * portfolio_value