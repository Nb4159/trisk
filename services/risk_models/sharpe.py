import numpy as np
class SharpeRatio:
    def calculate(returns, risk_free_rate=0.02):
        excess_returns = returns - risk_free_rate/252
        sharpe_ratio = (np.mean(excess_returns) / np.std(excess_returns))*np.sqrt(252   )
        return sharpe_ratio