# mlflow_test.py
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("test-experiment")

with mlflow.start_run():
    mlflow.log_param("param1", 5)
    mlflow.log_metric("accuracy", 0.93)
    print("Logged to MLflow!")
