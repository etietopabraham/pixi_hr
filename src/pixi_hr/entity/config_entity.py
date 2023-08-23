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