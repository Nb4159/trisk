import numpy as np
class SimulationMetrics:
    @staticmethod
    def summarize(paths):
        final_prices=paths.iloc[-1]
        return {
            "mean_price":float(np.mean(final_prices)),
            "median_price":float(np.median(final_prices)),
            "min_price":float(np.min(final_prices)),
            "max_price":float(np.max(final_prices)),    
            "p01"   :float(np.percentile(final_prices,1)),
            "p05"   :float(np.percentile(final_prices,5)),      
            "p95"   :float(np.percentile(final_prices,95)),
            "p99"   :float(np.percentile(final_prices,99))
            
        }