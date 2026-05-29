import mlflow
class MLFlowTracker:
    @staticmethod
    def start_run(run_name):
        mlflow.start_run(run_name=run_name)
    @staticmethod
    def log_params(key,value):
        mlflow.log_param(key,value)
    @staticmethod
    def log_metrics(key,value):
        mlflow.log_metric(key,value)
    @staticmethod
    def end_run():
        mlflow.end_run()