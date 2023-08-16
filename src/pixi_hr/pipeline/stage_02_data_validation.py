from pixi_hr import logger
from pixi_hr.config.configuration import ConfigurationManager
from pixi_hr.components.data_validation import DataValidation

class DataValidationTrainingPipeline:
    """
    Pipeline for validating the data before training or processing. 

    This pipeline performs the following steps:
    1. Initializes configuration management.
    2. Fetches the data validation configuration.
    3. Initializes the DataValidation component using the fetched configuration.
    4. Validates the columns of the data.
    """

    STAGE_NAME = "Data Validation Stage"

    def __init__(self):
        """
        Initializes the DataValidationTrainingPipeline.
        """
        pass

    def main(self):
        """
        Executes the main functionality of the DataValidationTrainingPipeline.
        """
        logger.info("Starting the Data Validation Pipeline...")

        # Step 1: Initialize ConfigurationManager
        logger.info("Initializing ConfigurationManager...")
        config = ConfigurationManager()

        # Step 2: Fetch Data Validation Configuration
        logger.info("Fetching Data Validation Configuration...")
        data_validation_config = config.get_data_validation_config()

        # Step 3: Initialize DataValidation Component
        logger.info("Initializing DataValidation Component...")
        data_validation = DataValidation(config=data_validation_config)

        # Step 4: Validate Columns
        logger.info("Validating Columns...")
        validation_status = data_validation.validate_columns()

        # Log the result of the validation
        if validation_status:
            logger.info("All columns successfully validated.")
        else:
            logger.warning("Column validation failed. Check logs for more details.")
        
        logger.info("Data Validation Pipeline completed successfully.")

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> Stage: {DataValidationTrainingPipeline.STAGE_NAME} started <<<<<<")
        data_validation_training_pipeline = DataValidationTrainingPipeline()
        data_validation_training_pipeline.main()
        logger.info(f">>>>>> Stage {DataValidationTrainingPipeline.STAGE_NAME} completed <<<<<< \n\nx==========x")
    except Exception as e:
        logger.exception(f"Error encountered during the Data Validation Pipeline: {e}")
        raise
