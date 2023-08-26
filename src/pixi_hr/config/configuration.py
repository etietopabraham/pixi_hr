from src.pixi_hr.constants import *
from src.pixi_hr.utils.common import read_yaml, create_directories

from pixi_hr.entity.config_entity import (DataIngestionConfig, 
                                          DataValidationConfig, 
                                          DataTransformationConfig, 
                                          ModelTrainerConfig,
                                          ModelEvaluationConfig)

class ConfigurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH,   # Path to the configuration YAML file
            params_filepath = PARAMS_FILE_PATH,   # Path to the parameters YAML file
            schema_filepath = SCHEMA_FILE_PATH):  # Path to the schema YAML file
        
        # Load the configuration details from the YAML file

        # print(type(config_filepath), config_filepath)
        
        self.config = read_yaml(config_filepath)
        # Load the parameters details from the YAML file
        self.params = read_yaml(params_filepath)
        # Load the schema details from the YAML file
        self.schema = read_yaml(schema_filepath)

        # Convert 'None' string to Python None object for specific parameters
        for param, value in self.params['RandomForest'].items():
            if value == 'None':
                self.params['RandomForest'][param] = None


        # Create directories as specified in the configuration (e.g., for storing artifacts)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        # Extract data ingestion configuration from the main configuration
        config = self.config.data_ingestion

        # Create directories specified in the data ingestion configuration
        create_directories([config.root_dir])

        # Create an instance of the DataIngestionConfig dataclass using the extracted configuration
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,               # Directory for data ingestion artifacts
            source_URL=config.source_URL,           # URL from which data will be downloaded
            local_data_file=config.local_data_file, # Local path where downloaded data will be saved
            unzip_dir=config.unzip_dir              # Directory where the zipped data will be extracted
        )

        return data_ingestion_config
    

    def get_data_validation_config(self) -> DataValidationConfig:
        # Extract data validation configuration from the main configuration
        config = self.config.data_validation
        # Extract schema columns from schema.yaml
        schema = self.schema.COLUMNS

        # Create directories specified in the data valition configuration
        create_directories([config.root_dir])

        # Create an instance of the DataValidationConfig dataclass using the extracted configuration
        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            unzip_data_dir=config.unzip_data_dir,
            STATUS_FILE=config.STATUS_FILE,
            validated_data_file=config.validated_data_file,
            all_schema=schema
        )

        return data_validation_config
    

    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Extracts the data transformation configuration from the main config.

        The function performs the following steps:
        1. Reads the data transformation section of the configuration.
        2. Ensures the specified root directory for data transformation exists (creates it if not).
        3. Returns a DataTransformationConfig object initialized with the extracted configuration.

        Returns:
        - DataTransformationConfig: A dataclass object containing the data transformation configuration.
        """
        
        # Extract the data transformation configuration from the main config
        config = self.config.data_transformation

        # Ensure the specified root directory for data transformation exists (creates it if not)
        create_directories([config.root_dir])

        # Create an instance of the DataTransformationConfig dataclass using the extracted configuration
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path
        )

        return data_transformation_config


    def get_model_trainer_config(self, chosen_model_type="RandomForest") -> ModelTrainerConfig:
        """
        Fetches the Model Trainer Configuration based on the chosen model type.

        Args:
        - chosen_model_type (str): The desired model type (either "ElasticNet" or "RandomForest").

        Returns:
            ModelTrainerConfig: A dataclass instance containing the model trainer configuration.
        """
        
        # Extract model trainer configuration
        config = self.config.model_trainer

        # Depending on the chosen model type, fetch the respective parameters
        if chosen_model_type == "ElasticNet":
            params = self.params.ElasticNet
        elif chosen_model_type == "RandomForest":
            params = self.params.RandomForest
        else:
            raise ValueError(f"Unsupported model type: {chosen_model_type}")
        
        schema = self.schema.TARGET_COLUMN

        # Create the directory where model training artifacts will be stored
        create_directories([config.root_dir])

        # Create an instance of the ModelTrainerConfig dataclass using the extracted configuration and parameters
        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            model_name=config.model_name,
            target_column=schema.name,
            model_type=chosen_model_type,
            model_params=params
        )

        return model_trainer_config
    

    def get_model_evaluation_config(self, chosen_model_type="RandomForest") -> ModelEvaluationConfig:
            """
            Fetches the configuration parameters required for the model evaluation stage based on the chosen model type.
            
            Args:
            - chosen_model_type (str): The desired model type (either "ElasticNet" or "RandomForest").
            
            Returns:
            - ModelEvaluationConfig: Dataclass containing the configuration parameters for the model evaluation stage.
            """
            config = self.config.model_evaluation

            # Depending on the chosen model type, fetch the respective parameters
            if chosen_model_type == "ElasticNet":
                params = self.params.ElasticNet
            elif chosen_model_type == "RandomForest":
                params = self.params.RandomForest
            else:
                raise ValueError(f"Unsupported model type: {chosen_model_type}")
                
            schema = self.schema.TARGET_COLUMN

            # Ensure the directory for model evaluation artifacts exists
            create_directories([config.root_dir])

            # Build the model evaluation configuration
            model_evaluation_config = ModelEvaluationConfig(
                root_dir=config.root_dir,
                test_data_path=config.test_data_path,
                model_path=config.model_path,
                metric_file_name=config.metric_file_name,
                all_params=params,
                target_column=schema.name,
                mlflow_uri=config.mlflow_uri
            )

            return model_evaluation_config
