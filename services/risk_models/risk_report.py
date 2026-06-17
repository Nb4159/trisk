from services.risk_models.var import ValueAtRisk
from services.risk_models.cvar import ConditionalVAR
from services.risk_models.drawdown import Drawdown
from services.risk_models.probability_metrics import ProbabilityMetrics

class CalculateRiskMetrics:
    def __init__(self,returns,initial_price,final_prices,paths):
        self.returns=returns
        self.initial_price=initial_price
        self.final_prices=final_prices
        self.paths=paths
    def generate_report(self):
        var95 = ValueAtRisk.monte_carlo(self.returns,confidence=0.95)
        var99 = ValueAtRisk.monte_carlo(self.returns,confidence=0.99)   
        cvar95 =ConditionalVAR.monte_carlo(self.returns,confidence=0.95)  
        cvar99 = ConditionalVAR.monte_carlo(self.returns,confidence=0.99)
        mean_path = self.paths.mean(axis=1)
        max_dd  = self.paths.apply(Drawdown.max_drawdown).mean()
        recovery_days =int(self.paths.apply(Drawdown.recovery_period).mean())
        prob_loss = ProbabilityMetrics.probability_of_loss(self.final_prices,self.initial_price)
        prob_10_loss = ProbabilityMetrics.probability_of_loss_pct(self.final_prices,self.initial_price,0.10)
        prob_20_gain = ProbabilityMetrics.probability_of_gain_pct(self.final_prices,self.initial_price,0.20) 
        risk_report = {

                "var_95": float(var95),
                "var_99": float(var99),

                "cvar_95": float(cvar95),
                "cvar_99": float(cvar99),

                "max_drawdown": float(max_dd),
                "recovery_days": int(recovery_days),

                "probability_of_loss":float(prob_loss),
                "probability_of_10pct_loss": float(prob_10_loss),
                "probability_of_20pct_gain":float(prob_20_gain)
            }
        return risk_report