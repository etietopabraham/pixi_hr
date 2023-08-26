import os
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from pathlib import Path

from pixi_hr.utils.common import save_json
from pixi_hr.config.configuration import ModelEvaluationConfig



class ModelEvaluation:
    """
    ModelEvaluation class for evaluating a trained predictive model.
    """

    def __init__(self, config: ModelEvaluationConfig):
        """
        Initializes the ModelEvaluation class with the given configuration.
        
        Args:
        - config (ModelEvaluationConfig): Configuration for the model evaluation.
        """
        self.config = config

    def eval_metrics(self, actual, predicted):
        """
        Computes evaluation metrics for the model's predictions.

        Args:
        - actual (pd.Series): Actual target values.
        - predicted (pd.Series): Predicted target values by the model.

        Returns:
        - tuple: RMSE, MAE, R2
        """
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mae = mean_absolute_error(actual, predicted)
        r2 = r2_score(actual, predicted)
        return rmse, mae, r2
    
    def load_data(self):
        """
        Load the test data and the trained model.
        """
        self.test_data = pd.read_csv(self.config.test_data_path)
        self.model = joblib.load(self.config.model_path)

    def preprocess_data(self):
        """
        Preprocesses the test data: Drops unwanted columns and splits data into features and target.
        """
        
        # Filter out columns that are not related to job_qualifications (i.e., prefixed by 'qual_')
        qualification_columns = [col for col in self.test_data.columns if col.startswith('qual_')]
        
        self.test_x = self.test_data[qualification_columns]
        self.test_y = self.test_data[self.config.target_column]


    def log_into_mlflow(self):
        """
        Logs model evaluation metrics and parameters into MLflow.
        """
        self.load_data()
        self.preprocess_data()

        # Set MLflow registry URI
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_score = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            predicted_qualities = self.model.predict(self.test_x)

            (rmse, mae, r2) = self.eval_metrics(self.test_y, predicted_qualities)
            scores = {"rmse": rmse, "mae": mae, "r2": r2}

            # Save evaluation metrics to JSON file using the utility function
            save_json(path=Path(self.config.metric_file_name), data=scores)

            # Log parameters and metrics into MLflow
            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2", r2)

            # Log model into MLflow
            if tracking_url_type_score != "file":
                mlflow.sklearn.log_model(self.model, "model", registered_model_name="ElasticnetModel")
            else:
                mlflow.sklearn.log_model(self.model, "model")