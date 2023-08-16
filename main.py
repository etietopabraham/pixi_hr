from pixi_hr import logger
from pixi_hr.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from pixi_hr.pipeline.stage_02_data_validation import DataValidationTrainingPipeline

def main():
    """
    Main execution method for the data processing and training pipelines.

    This method sequentially:
    1. Executes the data ingestion pipeline.
    2. Executes the data validation pipeline.

    Each pipeline has its own logging and error handling. If any pipeline fails,
    the error will be logged, and the entire program will terminate.
    """

    # List of pipeline stages to be executed
    pipelines = [DataIngestionTrainingPipeline(), DataValidationTrainingPipeline()]

    for pipeline in pipelines:
        try:
            # Start and log the current pipeline stage
            logger.info(f">>>>>> Stage: {pipeline.STAGE_NAME} started <<<<<<")
            pipeline.main()  # consistent method name across pipelines for execution
            logger.info(f">>>>>> Stage {pipeline.STAGE_NAME} completed <<<<<< \n\nx==========x")
        except Exception as e:
            # Log any errors encountered during the pipeline's execution
            logger.exception(f"Error encountered during the {pipeline.STAGE_NAME}: {e}")
            raise e

if __name__ == "__main__":
    main()
