from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd
import os
from pixi_hr import logger
from sklearn.ensemble import RandomForestRegressor


from pixi_hr.config.configuration import ModelTrainerConfig

class ModelTrainer:
    """
    ModelTrainer Class responsible for training a predictive model.
    
    Attributes:
        config (ModelTrainerConfig): Configuration for the model training.
    
    Methods:
        load_data: Load the training and testing datasets.
        preprocess_data: Preprocesses the data by dropping specific columns and splitting into features and target.
        scale_features: Scales the features using StandardScaler.
        train_model: Trains the model using the training data.
        save_model: Saves the trained model to a specified directory.
        main: Orchestrates the model training process.
    """

    def __init__(self, config: ModelTrainerConfig):
        """
        Initializes the ModelTrainer class with a configuration.

        Args:
            config (ModelTrainerConfig): Configuration for model training.
        """
        self.config = config

    def load_data(self):
        """Load training and test data."""
        self.train_data = pd.read_csv(self.config.train_data_path)
        self.test_data = pd.read_csv(self.config.test_data_path)

    def print_data(self):
        print("Scaled Train Features")
        print(pd.DataFrame(self.train_x).head())
        print("Scaled Test Features")
        print(pd.DataFrame(self.test_x).head())



    def preprocess_data(self):
        """Drop unwanted columns and split data into features and target."""
        
        # Filter out columns that are not related to job_qualifications (i.e., prefixed by 'qual_')
        qualification_columns = [col for col in self.train_data.columns if col.startswith('qual_')]
        
        self.train_x = self.train_data[qualification_columns]
        self.train_y = self.train_data[self.config.target_column]

        self.test_x = self.test_data[qualification_columns]
        self.test_y = self.test_data[self.config.target_column]


    def scale_features(self):
        """Scale the features using StandardScaler."""
        scaler = StandardScaler()
        self.train_x = scaler.fit_transform(self.train_x)
        self.test_x = scaler.transform(self.test_x)

    def train_model(self, model):
        """
        Train the model using the training data.

        Args:
            model (model instance): Machine learning model to be trained.
        
        Returns:
            model (model instance): Trained machine learning model.
        """
        model.fit(self.train_x, self.train_y)
        return model

    def save_model(self, model):
        """
        Save the trained model to a specified directory.

        Args:
            model (model instance): Trained machine learning model to save.
        """
        try:
            joblib.dump(model, os.path.join(self.config.root_dir, self.config.model_name))
            logger.info(f"Model saved successfully at {os.path.join(self.config.root_dir, self.config.model_name)}")
        except Exception as e:
            logger.error(f"Error saving the model: {e}")
            raise e

    def main(self):

        """Main execution method that orchestrates the model training process."""
        
        logger.info("Loading data...")
        self.load_data()
        
        logger.info("Preprocessing data...")
        self.preprocess_data()

        # Depending on the model type from the configuration, initialize the appropriate model
        if self.config.model_type == "ElasticNet":
            model = ElasticNet(
                alpha=self.config.model_params["alpha"], 
                l1_ratio=self.config.model_params["l1_ratio"], 
                random_state=44
            )
        elif self.config.model_type == "RandomForest":
            model = RandomForestRegressor(
                n_estimators=self.config.model_params["n_estimators"],
                max_depth=self.config.model_params["max_depth"],
                min_samples_split=self.config.model_params["min_samples_split"],
                min_samples_leaf=self.config.model_params["min_samples_leaf"],
                max_features=self.config.model_params["max_features"],
                random_state=self.config.model_params["random_state"]
            )
        else:
            raise ValueError(f"Unsupported model type: {self.config.model_type}")
        
        trained_model = self.train_model(model)
        
        logger.info("Saving the trained model...")
        self.save_model(trained_model)
        