import numpy as np
import pandas as pd
class Drawdown:
    @staticmethod
    def calculate(price_series):
        running_max = price_series.cummax()
        drawdown = (price_series - running_max) / running_max   
        return drawdown
    @staticmethod
    def max_drawdown(price_series):
        drawdown = Drawdown.calculate(price_series)
        return drawdown.min()
    @staticmethod
    def recovery_period(price_series):
        running_max = price_series.cummax()
        underwater = price_series < running_max
        longest=0
        current=0
        for val in underwater:
            if val:
                current += 1
                longest = max(longest,current)
            else:
                current = 0
        return longest