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
