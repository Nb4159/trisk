from scipy.stats import jarque_bera
class Diagnostics:

    @staticmethod
    def normality_test(series):

        stat, p = jarque_bera(
            series.dropna()
        )

        return {
            "jb_stat": stat,
            "p_value": p
        }