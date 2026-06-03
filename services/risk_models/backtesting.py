import pandas as pd
import numpy as np
from scipy.stats import chi2
class VarBacktester:
    @staticmethod
    def violation_rate(returns,var_series):
        returns = pd.Series(returns).dropna()
        var_series = pd.Series(var_series).dropna()
        violations=returns.values < -var_series.values
        cnt=violations.sum()
        rate=cnt/len(returns)
        return {
            "violations": int(cnt),
            "total": len(returns),
            "violation_rate": rate
        }
    @staticmethod
    def kupiec_test(returns,var_series,confidence=0.95):
        returns = pd.Series(returns).dropna()
        var_series = pd.Series(var_series).dropna()
        violations=int((returns.values < -var_series.values).sum())
        p_exp=1-confidence
        p_obs=violations/len(returns)
        expected=len(returns)*p_exp
        if expected==0 or expected==len(returns):
            return {
                "expected_violations":
                    round(expected, 2),
                "actual_violations":
                    violations,
                "kupiec_stat":
                    None,
                "p_value":
                    None,
                "passed":
                    False
            }
        n=len(returns)
        lr_stat = -2 * (

            (n - violations)
            * np.log(
                (1 - p_exp)
                / (1 - p_obs)
            )

            +

            violations
            * np.log(
                p_exp
                / p_obs
            )

        )
        p_value = 1 - chi2.cdf(lr_stat, df=1)
        return {
            "expected_violations":
                round(expected, 2),

            "actual_violations":
                violations,

            "kupiec_stat":
                round(float(lr_stat), 6),

            "p_value":
                round(float(p_value), 6),

            "passed":
                bool(p_value > 0.05)
        }
    #Add bessel later on
    def summary(
        returns: pd.Series, var_series: pd.Series, confidence: float = 0.95) -> dict:
       
        violation_stats = VarBacktester.violation_rate(returns, var_series)
        kupiec_stats    = VarBacktester.kupiec_test(returns, var_series, confidence)

        return {
            **violation_stats,
            **kupiec_stats
        }
