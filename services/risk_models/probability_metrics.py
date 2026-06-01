import pandas as pd
class ProbabilityMetrics:

    @staticmethod
    def probability_of_loss(
        final_prices: pd.Series,
        initial_price: float
    ) -> float:

        return (
            (final_prices < initial_price)
            .mean()
        )

    @staticmethod
    def probability_of_loss_pct(
        final_prices: pd.Series,
        initial_price: float,
        loss_pct: float = 0.10
    ) -> float:

        threshold = (
            initial_price *
            (1 - loss_pct)
        )

        return (
            (final_prices < threshold)
            .mean()
        )

    @staticmethod
    def probability_of_gain_pct(
        final_prices: pd.Series,
        initial_price: float,
        gain_pct: float = 0.20
    ) -> float:

        threshold = (
            initial_price *
            (1 + gain_pct)
        )

        return (
            (final_prices > threshold)
            .mean()
        )