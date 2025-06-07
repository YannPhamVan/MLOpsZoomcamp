FROM python:3.11-slim

# Installation de MLflow en version 2.12.1
RUN pip install mlflow==2.12.1

# Création du dossier de stockage des artefacts
ENV MLFLOW_ARTIFACT_ROOT=/home/mlflow_data
RUN mkdir -p $MLFLOW_ARTIFACT_ROOT

# Lancement du serveur MLflow
CMD mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri $MLFLOW_ARTIFACT_ROOT \
    --default-artifact-root $MLFLOW_ARTIFACT_ROOT
