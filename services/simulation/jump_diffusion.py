import pandas as pd
import numpy as np

class JumpDiffusionSimulator:
    def __init__(self,initial_price,mu,volatility_path,jump_lambda,jump_mu,jump_sigma,simulations=5000,seed=42):
        self.s0=initial_price
        self.mu=mu
        self.volatility_path=np.asarray(volatility_path)
        self.jump_lambda=jump_lambda
        self.jump_mu=jump_mu
        self.jump_sigma=jump_sigma
        self.simulations=simulations
        self.rng = np.random.default_rng(seed)
    def simulate(self):
        horizon=len(self.volatility_path)
        dt=1/252
        paths=np.zeros((horizon+1,self.simulations))
        paths[0]=self.s0
        for t in range(1,horizon+1):
            sigma_t=self.volatility_path[t-1]/100
            z=np.random.normal(0,1,self.simulations)
            diffusion=(self.mu-0.5*sigma_t**2)*dt+sigma_t*np.sqrt(dt)*z
            jump_cnt=np.random.poisson(self.jump_lambda*dt,self.simulations)
            jump_sizes=(np.random.normal(self.jump_mu,self.jump_sigma,self.simulations))
            jump_component=jump_cnt*jump_sizes
            paths[t]=paths[t-1]*np.exp(diffusion+jump_component)
        return pd.DataFrame(paths)
    