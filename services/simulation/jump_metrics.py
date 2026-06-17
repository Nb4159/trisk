import numpy as np
class JumpMetrics:
    @staticmethod
    def compare_tail_risk(gbm_returns, jump_returns):
        gbm_var95 = np.percentile(gbm_returns, 5)
        jump_var95 = np.percentile(jump_returns, 5)
        gbm_cvar95 = gbm_returns[gbm_returns <= gbm_var95].mean()
        jump_cvar95= jump_returns[jump_returns<=jump_var95].mean()

        return {
            "gbm_var95": gbm_var95,
            "jump_var95": jump_var95,
            "gbm_cvar95": gbm_cvar95,
            "jump_cvar95": jump_cvar95,
            "tail_risk_multiplier":abs(jump_cvar95/gbm_cvar95) if gbm_cvar95!=0 else float('inf')
        }