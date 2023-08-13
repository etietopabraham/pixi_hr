import os
import urllib.request as request
import zipfile
from pixi_hr import logger
from pixi_hr.utils.common import get_size
from pathlib import Path
from pixi_hr.entity.config_entity import (DataIngestionConfig)

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        """
        Initialize the DataIngestion class with the provided configuration.
        
        Args:
            config (DataIngestionConfig): Configuration for data ingestion.
        """
        self.config = config

    def download_file(self):
        """
        Downloads the data file from the specified source URL to a local path.
        If the file already exists locally, logs its size without re-downloading.
        """
        
        # Check if the data file already exists locally
        if not os.path.exists(self.config.local_data_file):
            # If not, download the file
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"Downloaded {filename} with the following information: \n {headers}")
        else:
            # If file exists, log its size
            file_size = get_size(Path(self.config.local_data_file))
            logger.info(f"File already exists of size: {file_size}")

    
    def extract_zip_file(self) -> None:
        """
        Extracts the contents of the downloaded ZIP file to a specified directory.
        
        Returns:
            None
        """
        
        # Ensure the directory for extraction exists or create it
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        # Extract the contents of the ZIP file
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)



