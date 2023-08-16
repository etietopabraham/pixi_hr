import os
import pandas as pd
from pixi_hr import logger
from pixi_hr.entity.config_entity import DataValidationConfig

class DataValidation:
    """
    Data Validation class to ensure data quality and integrity.
    
    Attributes:
    - config (DataValidationConfig): Configuration object containing paths and schema information.
    - df (DataFrame): Pandas DataFrame loaded from the specified data file.
    """

    def __init__(self, config: DataValidationConfig):
        """
        Initializes the DataValidation class.

        Args:
        - config (DataValidationConfig): Configuration object containing paths and schema information.
        """
        self.config = config
        try:
            # Load the data into a DataFrame
            self.df = pd.read_csv(self.config.unzip_data_dir)
        except FileNotFoundError:
            logger.error(f"File not found: {self.config.unzip_data_dir}")
            raise
        except Exception as e:
            logger.error(f"Error reading data file: {e}")
            raise

    def validate_columns(self) -> bool:
        """
        Validate if all expected columns are present in the dataset.
        Logs missing or extra columns and writes the validation status 
        to a specified file.

        Returns:
        - bool: True if all columns are as expected, False otherwise.
        """
        # Initialize the validation status and the status message
        validation_status = True
        status_message = "Validation status: "
        
        # Determine missing or extra columns
        all_columns = set(self.df.columns)
        expected_columns = set(self.config.all_schema.keys())
        missing_columns = expected_columns - all_columns
        extra_columns = all_columns - expected_columns
        
        # Log and update the status message for any discrepancies
        if missing_columns:
            validation_status = False
            logger.warning(f"Missing columns: {', '.join(missing_columns)}")
            status_message += f"Missing columns: {', '.join(missing_columns)}\n"
        if extra_columns:
            validation_status = False
            logger.warning(f"Extra columns found: {', '.join(extra_columns)}")
            status_message += f"Extra columns found: {', '.join(extra_columns)}\n"
        if validation_status:
            logger.info("All expected columns are present in the dataframe.")
            status_message += "All expected columns are present."
        
        # Write the validation status to the file
        self._write_status_to_file(status_message)

        return validation_status

    def _write_status_to_file(self, message: str):
        """
        Writes a given message to the status file specified in the config.

        Args:
        - message (str): The message to write.
        """
        try:
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(message)
        except Exception as e:
            logger.error(f"Error writing to status file: {e}")
            raise
