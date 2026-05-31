import numpy as np
class ReturnEstimator:
    @staticmethod
    def annualized_return( returns):
        return (np.mean(returns)* 252)