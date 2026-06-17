import numpy as np
import pandas as pd
class JumpCalibration:
    @staticmethod
    def calibrate(returns,threshold_std=3.0):
        returns=returns.dropna()
        sigma=returns.std()
        jumps=returns[np.abs(returns)>threshold_std*sigma]
        cnt=len(jumps)
        jump_lambda=cnt/len(returns)
        if cnt>0:
            jump_mu=jumps.mean()
            jump_sigma=jumps.std()
        else:
            jump_mu=0.0
            jump_sigma=sigma
        return {
            "jump_lambda": jump_lambda,
            "jump_mu": jump_mu,
            "jump_sigma": jump_sigma,
            "jump_count": cnt   
            
        }