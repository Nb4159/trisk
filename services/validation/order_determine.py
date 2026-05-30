import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
class ACF_PACF:
    @staticmethod
    def generate(series, lags=50,save_path="outputs/figures/acf_pacf.png"):
        fig, axes = plt.subplots(1, 2, figsize=(12, 8))
        plot_acf(series.dropna(), lags=lags, ax=axes[0])
        plot_pacf(series.dropna(), lags=lags, ax=axes[1])
        plt.tight_layout()
        plt.savefig(save_path) 
        plt.show()