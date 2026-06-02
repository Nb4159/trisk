# services/simulation/jump_diffusion.py

import numpy as np
import pandas as pd


class JumpDiffusionSimulator:

    def __init__(
        self,
        initial_price,
        mu,
        sigma,
        jump_lambda=0.10,
        jump_mu=-0.05,
        jump_sigma=0.15,
        horizon=252,
        simulations=5000,
        seed=42
    ):

        self.S0 = initial_price
        self.mu = mu
        self.sigma = sigma

        self.jump_lambda = jump_lambda
        self.jump_mu = jump_mu
        self.jump_sigma = jump_sigma

        self.horizon = horizon
        self.simulations = simulations

        np.random.seed(seed)

    def simulate(self):

        dt = 1 / 252

        paths = np.zeros(
            (self.horizon + 1,
             self.simulations)
        )

        paths[0] = self.S0

        for t in range(1, self.horizon + 1):

            z = np.random.normal(
                0,
                1,
                self.simulations
            )

            poisson = np.random.poisson(
                self.jump_lambda * dt,
                self.simulations
            )

            jump_size = np.exp(
                np.random.normal(
                    self.jump_mu,
                    self.jump_sigma,
                    self.simulations
                )
            )

            jump_component = (
                jump_size - 1
            ) * poisson

            diffusion = (
                (self.mu -
                 0.5*self.sigma**2)*dt
                +
                self.sigma *
                np.sqrt(dt) * z
            )

            paths[t] = (
                paths[t-1]
                * np.exp(diffusion)
                * (1 + jump_component)
            )

        return pd.DataFrame(paths)