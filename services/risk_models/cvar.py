import numpy as np
import pandas as pd

class ConditionalVAR:
    @staticmethod
    def historical(returns, confidence=0.95):
        var=np.percentile(returns.dropna(),(1-confidence)*100)
        tail_losses = returns[returns <= var]
        return -tail_losses.mean()
    @staticmethod
    def monte_carlo(simulated_returns, confidence=0.95):
        var=np.percentile(simulated_returns.dropna(),(1-confidence)*100)
        tail_losses = simulated_returns[simulated_returns <= var]
        return -tail_losses.mean()