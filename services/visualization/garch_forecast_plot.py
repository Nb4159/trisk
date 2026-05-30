import plotly.express as px
import pandas as pd
class GARCHForecastPlot:
    @staticmethod
    def plot(forecasted_volatility, ticker, save_path=None):
        if save_path is None:
            save_path = f"outputs/figures/{ticker}_garch_forecast_plot.html"
        forecasted_df=pd.DataFrame({"step":range(1,len(forecasted_volatility)+1),
                                    "forecasted_volatility":forecasted_volatility})
        fig=px.line(forecasted_df, x="step", y="forecasted_volatility",markers=True, title=f"{ticker} GARCH Forecasted Volatility Over Time")
        fig.write_html(save_path)