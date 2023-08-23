from src.pixi_hr.constants import *
from src.pixi_hr.utils.common import read_yaml, create_directories

from pixi_hr.entity.config_entity import (DataIngestionConfig, DataValidationConfig, DataTransformationConfig)

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
