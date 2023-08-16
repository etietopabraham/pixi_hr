import os
import pandas as pd
import ast  # Required for the validate_job_qualifications method
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

    
    def validate_date_of_job_post(self):
        """
        Validate that 'date_of_job_post' contains valid date-time strings.
        Logs any discrepancies.
        """
        try:
            self.df['date_of_job_post_temp'] = pd.to_datetime(self.df['date_of_job_post'], errors='raise')
            logger.info("All values in 'date_of_job_post' are valid date-time strings.")
        except Exception as e:
            logger.warning(f"Error encountered: {e}")
            self.df['date_of_job_post_temp'] = pd.to_datetime(self.df['date_of_job_post'], errors='coerce')
            invalid_rows = self.df[self.df['date_of_job_post_temp'].isna()]
            logger.warning("\nRows with invalid date-time strings:")
            logger.warning(invalid_rows[['date_of_job_post']])

    
    def validate_text_fields(self, columns):
        """
        Validate that the specified columns contain only text values.
        Logs any columns containing non-text values.

        Args:
        - columns (list): List of column names to validate.
        """
        for column in columns:
            non_text_rows = self.df[self.df[column].apply(lambda x: not isinstance(x, str))]
            if not non_text_rows.empty:
                logger.warning(f"Column '{column}' has non-text values:")
                logger.warning(non_text_rows[[column]])
            else:
                logger.info(f"Column '{column}' contains only text values.")

    
    def validate_job_link(self):
        """
        Validate that 'job_link' starts with "http".
        Logs any URLs not starting with 'http'.
        """
        invalid_urls = self.df[~self.df['job_link'].str.startswith("http")]
        if not invalid_urls.empty:
            logger.warning(f"Found {len(invalid_urls)} rows with URLs not starting with 'http':")
            logger.warning(invalid_urls[['job_link']])
        else:
            logger.info("All URLs in 'job_link' start with 'http'.")


    def validate_job_type(self):
        """
        Validate that 'job_type' contains only text values, excluding nulls.
        Logs any non-text values found.
        """
        non_null_job_types = self.df[self.df['job_type'].notna()]
        non_text_job_types = non_null_job_types[~non_null_job_types['job_type'].apply(lambda x: isinstance(x, str))]
        if not non_text_job_types.empty:
            logger.warning(f"Found {len(non_text_job_types)} rows in 'job_type' with non-text values:")
            logger.warning(non_text_job_types[['job_type']])
        else:
            logger.info("All non-null values in 'job_type' are of text type.")

    
    def validate_job_qualifications(self):
        """
        Validate that 'job_qualifications' contains valid lists of text values.
        Logs any invalid format found.
        """
        def is_valid_list(value):
            try:
                lst = ast.literal_eval(value)
                return isinstance(lst, list) and all(isinstance(i, str) for i in lst)
            except (ValueError, SyntaxError):
                return False

        invalid_qualifications = self.df[~self.df['job_qualifications'].apply(is_valid_list)]
        if not invalid_qualifications.empty:
            logger.warning(f"Found {len(invalid_qualifications)} rows in 'job_qualifications' with invalid format:")
            logger.warning(invalid_qualifications[['job_qualifications']])
        else:
            logger.info("All values in 'job_qualifications' are valid lists of text values.")


    def handle_duplicates(self):
        """
        Handle duplicate rows based on the 'job_link' column.
        Logs the number of duplicates found and handled.
        """
        num_duplicates = self.df[self.df['job_link'].duplicated()].shape[0]
        if num_duplicates > 0:
            self.df.drop_duplicates(subset='job_link', inplace=True)
            logger.info(f"Dropped {num_duplicates} duplicate rows based on the 'job_link' column.")
        else:
            logger.info("No duplicates found based on the 'job_link' column.")