from prefect import flow, task
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
import cloudpickle
import requests
import joblib

@task
def extract(url: str, output_path: str):
    r = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(r.content)
    return output_path

@task
def prepare_data(input_path: str, output_path: str):
    df = pd.read_parquet(input_path)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df['duration'].dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].fillna(-1).astype(int).astype(str)
    df[categorical + ["duration"]].to_parquet(output_path, index=False)
    return output_path

@task
def train_model(input_path: str):
    mlflow.set_tracking_uri("http://localhost:5000")
    experiment_name = "nyc-taxi-experiment"
    mlflow.set_experiment(experiment_name)

    df = pd.read_parquet(input_path)
    categorical = ["PULocationID", "DOLocationID"]
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    y_train = df["duration"].values

    with mlflow.start_run():
        lr = LinearRegression()
        lr.fit(X_train, y_train)

        mlflow.sklearn.log_model(lr, artifact_path="model")
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("features", categorical)

        df.to_parquet("filtered_logged.parquet", index=False)
        mlflow.log_artifact("filtered_logged.parquet")

        joblib.dump(dv, "dv.pkl")
        mlflow.log_artifact("dv.pkl")

@flow(name="q6_register_model_prefect")
def main_flow():
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet"
    raw_path = "data.parquet"
    filtered_path = "filtered.parquet"

    extract_path = extract(url, raw_path)
    filtered_path = prepare_data(extract_path, filtered_path)
    train_model(filtered_path)

if __name__ == "__main__":
    main_flow()
