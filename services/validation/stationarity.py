from statsmodels.tsa.stattools import adfuller
class StationarityTest:
    @staticmethod
    def adf_test(series):
        result=adfuller(series.dropna())
        return {
            'adf_statistic': result[0],
            'p-value': result[1],   
            'critical_values': result[4]
        }