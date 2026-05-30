import plotly.express as px

class RollingVolatilityPlot:
    @staticmethod
    def plot(df,ticker,plot_path):
        fig=px.line(df,x=df.index,y=df[('rolling_volatility', '')],title=f"{ticker} Rolling Volatility")
        fig.write_html(plot_path)