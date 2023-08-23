from pathlib import Path

from pixi_hr import logger
from pixi_hr.config.configuration import ConfigurationManager 
from pixi_hr.components.data_transformation import DataTransformationConfig, DataTransformation

class DataTransformationPipeline:
    """
    Data Transformation Pipeline for preparing data for modeling.

    The pipeline checks the validation status from the previous stage 
    to ensure that the data is ready for transformation. 
    If the validation status is passed, the data is transformed 
    and made ready for the next stages in the ML workflow.

    Attributes:
        STAGE_NAME (str): Name of the pipeline stage.
    """
    
    STAGE_NAME = "Data Transformation Stage"

    def main(self):
        """
        Main execution method for the Data Transformation Pipeline.

        It checks the validation status, and if the data is validated successfully, 
        it initiates the data transformation process.
        """
        try:
            # Check the validation status
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                status = f.read().split("\n")[-1]

            if "All expected columns are present." in status:
                logger.info("Starting the Data Transformation Pipeline")

                # Step 1: Initialize Configuration Manager
                logger.info("Initializing configuration manager")
                config = ConfigurationManager()

                # Step 2: Fetch Data Transformation Configuration
                logger.info("Fetching Data Transformation Configuration..")
                data_transformation_config = config.get_data_transformation_config()

                # Step 3: Initialize Data Transformation Component
                logger.info("Initializing Data Transformation Component...")
                data_transformation = DataTransformation(config=data_transformation_config)

                # Step 4: Transform Data
                logger.info("Transforming data...")
                data_transformation.main()

                logger.info("Data Transformation Pipeline completed successfully.")
            else:
                logger.error("Data schema is not valid, all columns are not present.")
                raise Exception("Data schema is not valid, all columns are not present. Please check validation status in artifacts/data_validation/status.txt")
        
        except Exception as e:
            logger.exception(f"Error encountered during the Data Transformation Pipeline: {e}")
            raise

if __name__ == '__main__':
    logger.info(f">>>>>> Stage: {DataTransformationPipeline.STAGE_NAME} started <<<<<<")
    data_transformation_pipeline = DataTransformationPipeline()
    data_transformation_pipeline.main()
    logger.info(f">>>>>> Stage {DataTransformationPipeline.STAGE_NAME} completed <<<<<< \n\nx==========x")
