import numpy as np
import pandas as pd
seed=42
class GBMSimulator:
    def __init__(
        self,
        initial_price,
        mu,
        volatility_path,
        simulations
    ):

        self.initial_price = initial_price
        self.mu = mu
        self.volatility_path = volatility_path
        self.simulations = simulations

    def simulate(self):

        rng = np.random.default_rng(seed)
        horizon = len(self.volatility_path)
        paths = np.zeros((horizon + 1, self.simulations))
        paths[0] = self.initial_price
        dt = 1 / 252

        for t in range(1, horizon + 1):

            sigma_t = self.volatility_path[t - 1] / 100

            half = (self.simulations + 1) // 2
            z_half = rng.standard_normal(half)
            z = np.concatenate([z_half, -z_half])[:self.simulations]

            paths[t] = (
                paths[t - 1]
                * np.exp(
                    (self.mu - 0.5 * sigma_t**2) * dt
                    + sigma_t * np.sqrt(dt) * z
                )
            )

        return pd.DataFrame(paths)
