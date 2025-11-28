# MLFlow-training

Repository that containts code related to my MLFlow training.

MLflow is an open-source platform for managing the machine learning lifecycle. It helps teams track experiments, package models, and deploy them efficiently. Its main components are:

- Tracking – Log and compare parameters, metrics, and artifacts from ML experiments.
- Projects – Define reproducible ML workflows using a standard format.
- Models – Package ML models for deployment in various environments.
- Model Registry – Manage versions of models, including staging and production.

## Project
My project is develop in python, with a Makefile that ensures all dependencies are correctly installed in a virtual environment to allow for containerized reproducibility.
There are 3 scripts:
- "mlflow-hptuning.py" that performs hyperparameter tuning on a random forest model that fits housing prices data, selecting the best model based on a simple error criteria.
- "mlflow-staging.py" that sets the development stage of the model within airflow.
- "mlflow-inferencing.py" that infers the MLFlow server on the prediction the fitted model outputs for a given feature data point.
