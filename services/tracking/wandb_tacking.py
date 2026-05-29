import wandb
class WandbTracker:
    @staticmethod
    def init(self, project_name):
        self.project_name = project_name
        wandb.init(project=self.project_name)
    @staticmethod
    def log(self, metrics:dict):
        wandb.log(metrics)
    @staticmethod
    def finish(self):
        wandb.finish()