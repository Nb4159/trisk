from arch import arch_model
import pandas as pd
import numpy as np
class GARCHModel:
    def __init__(self,returns:pd.Series):
        self.returns=returns*100
    def fit(self,p,q):
        model=arch_model(self.returns,vol="Garch",p=p,q=q,dist="t")
        return model.fit(disp="off")
    def forecast_volatility(self,model,horizon=252):
        forecast=model.forecast(horizon=horizon)
        variances = (
            forecast
            .variance
            .iloc[-1]
            .values
        )

        volatilities = np.sqrt(
            variances
        )

        return volatilities
        return forecast.variance.values[-1]
    