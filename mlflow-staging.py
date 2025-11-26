import mlflow

client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
        name="best_random_forest",
        version = 1,
        stage="Production",
    )
