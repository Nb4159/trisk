from arch import arch_model
import pandas as pd
class GARCHModel:
    def __init__(self,returns:pd.Series):
        self.returns=returns*100
    def fit(self,p,q):
        model=arch_model(self.returns,vol="Garch",p=p,q=q)
        return model.fit(disp="off")
    def forecast_volatility(self,model,horizon=5):
        forecast=model.forecast(horizon=horizon)
        return forecast.variance.values[-1]
    