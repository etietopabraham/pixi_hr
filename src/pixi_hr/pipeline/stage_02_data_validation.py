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
    4. Validates the columns and other aspects of the data.
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

        # Step 4: Execute all validation functions
        logger.info("Executing Data Validations...")

        validations = [
            ("Column Validation", data_validation.validate_columns),
            ("Date of Job Post Validation", data_validation.validate_date_of_job_post),
            ("Text Fields Validation", lambda: data_validation.validate_text_fields(
                columns=['title', 'company_name', 'job_location', 'job_summary', 'job_description']  # or any other columns you'd like to validate
            )),
            ("Job Link Validation", data_validation.validate_job_link),
            ("Job Type Validation", data_validation.validate_job_type),
            ("Job Qualifications Validation", data_validation.validate_job_qualifications),
            ("Duplicate Entries Handling", data_validation.handle_duplicates)
        ]

        for validation_name, validation_function in validations:
            logger.info(f"Executing {validation_name}...")
            validation_function()

        logger.info("All validations completed successfully.")
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
