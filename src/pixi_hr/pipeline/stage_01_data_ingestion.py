from pixi_hr.config.configuration import ConfigurationManager
from pixi_hr.components.data_ingestion import DataIngestion
from pixi_hr import logger


STAGE_NAME = "Data Ingestion State"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    
    def main(self):
        try:
            # Initialize configuration manager to fetch relevant configurations
            config = ConfigurationManager()
            
            # Fetch the data ingestion-specific configuration
            data_ingestion_config = config.get_data_ingestion_config()
            
            # Initialize the data ingestion process with the fetched configuration
            data_ingestion = DataIngestion(config=data_ingestion_config)
            
            # Download the data file from the specified source
            data_ingestion.download_file()
            
            # Extract the downloaded ZIP file to the specified directory
            data_ingestion.extract_zip_file()

        except Exception as e:
            # If any error occurs during the process, raise the exception to handle or log it appropriately
            logger.info(f"An exception {e} has occured")
            raise e


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> Stage: {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<< \n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e