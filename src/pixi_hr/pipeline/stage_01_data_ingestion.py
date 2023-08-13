from pixi_hr.config.configuration import ConfigurationManager
from pixi_hr.components.data_ingestion import DataIngestion
from pixi_hr import logger


class DataIngestionTrainingPipeline:
    """
    Pipeline to manage the data ingestion process for training.
    """
    
    STAGE_NAME = "Data Ingestion State"

    def main(self):
        """
        Main execution method for the data ingestion pipeline.
        """
        try:
            logger.info("Initializing configuration manager...")
            # Initialize configuration manager to fetch relevant configurations
            config = ConfigurationManager()
            
            logger.info("Fetching data ingestion configuration...")
            # Fetch the data ingestion-specific configuration
            data_ingestion_config = config.get_data_ingestion_config()
            
            logger.info("Initializing data ingestion process...")
            # Initialize the data ingestion process with the fetched configuration
            data_ingestion = DataIngestion(config=data_ingestion_config)
            
            logger.info("Downloading data file...")
            # Download the data file from the specified source
            data_ingestion.download_file()
            
            logger.info("Extracting ZIP file...")
            # Extract the downloaded ZIP file to the specified directory
            data_ingestion.extract_zip_file()

        except Exception as e:
            # Log the exception with its traceback
            logger.exception("An error occurred during the data ingestion process.")
            raise e


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> Stage: {DataIngestionTrainingPipeline.STAGE_NAME} started <<<<<<")
        pipeline = DataIngestionTrainingPipeline()
        pipeline.main()
        logger.info(f">>>>>> Stage {DataIngestionTrainingPipeline.STAGE_NAME} completed <<<<<< \n\nx==========x")
    except Exception as e:
        # No need to log the exception here since it's already logged in the main method.
        raise e
