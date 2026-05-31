import plotly.graph_objects as go
class MonteCarloPlotter:
    @staticmethod
    def plot(
        paths,
        ticker,
        save_path
    ):

        fig = go.Figure()

        max_paths = min(
            100,
            paths.shape[1]
        )

        for i in range(max_paths):

            fig.add_trace(
                go.Scatter(
                    y=paths.iloc[:, i],
                    mode="lines",
                    showlegend=False
                )
            )

        fig.update_layout(
            title=f"{ticker} GBM Simulations",
            xaxis_title="Day",
            yaxis_title="Price"
        )

        fig.write_html(save_path)