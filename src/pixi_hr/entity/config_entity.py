from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    # Directory where data ingestion artifacts are stored
    root_dir: Path
    # URL from which data will be downloaded
    source_URL: str
    # Path to the local file where downloaded data will be saved
    local_data_file: Path
    # Directory where the zipped data will be extracted
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    # Path to the root directory where data validation artifacts are stored.
    root_dir: Path
    
    # Location of the extracted data (in this case, a CSV file) that needs to be validated.
    unzip_data_dir: Path
    
    # Path to a status file used to track the progress or status of data validation.
    STATUS_FILE: str

    # Location of the validated data.
    validated_data_file: Path
    
    # Store all schema configuration
    all_schema: dict


@dataclass(frozen=True)
class DataTransformationConfig:
    """
    Configuration entity for the Data Transformation pipeline.
    
    This configuration entity provides necessary paths and directories 
    related to data transformation activities.
    
    Attributes:
    - root_dir (Path): The root directory where data transformation artifacts are stored.
    - data_path (Path): The path to the dataset (typically CSV) that needs to be transformed.
    """

    # Root directory for storing transformation-related artifacts
    root_dir: Path

    # Path to the validated dataset for transformation
    data_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    """
    Configuration entity for the Model Trainer.

    Attributes:
    - root_dir: Directory where model training artifacts will be stored.
    - train_data_path: Path to the training data file.
    - test_data_path: Path to the test data file.
    - model_name: Name of the model file to be saved.
    - alpha: Regularization strength for the ElasticNet model. 
             Combines the L1 and L2 penalties. Higher values specify stronger regularization.
    - l1_ratio: The mix between L1 and L2 regularization. 
                0 <= l1_ratio <= 1. 0 corresponds to L2 (Ridge) and 1 to L1 (Lasso).
    - target_column: Name of the column in the dataset that represents the target variable.
    """

    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    model_type: str
    model_params: dict
    target_column: str

    

    



@dataclass(frozen=True)
class ModelEvaluationConfig:
    """Configuration parameters for the model evaluation stage."""

    # Root directory to store evaluation artifacts
    root_dir: Path

    # Path to the test dataset (output from the data transformation stage)
    test_data_path: Path

    # Path to the trained model (output from the model trainer stage)
    model_path: Path

    # File path to save computed evaluation metrics in JSON format
    metric_file_name: Path

    # Dictionary containing all the parameters for model evaluation
    all_params: dict

    # Name of the target column in the dataset
    target_column: str

    # URI for the MLFlow server or database
    mlflow_uri: str

