import plotly.express as px
class PricePlot:
    @staticmethod
    def plot(df,ticker,save_path=None):
        if save_path is None:
            save_path = f"outputs/figures/{ticker}_plot.html"
        fig=px.line(df,x=df.index,y=df[("Close", ticker)] ,title=f"{ticker} Price Over Time")
        fig.write_html(save_path)
