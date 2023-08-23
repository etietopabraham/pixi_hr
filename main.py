"""
Main execution script for the entire ML workflow, starting from data ingestion 
to data transformation. Each stage in the workflow is represented as a pipeline 
and is executed sequentially.
"""

from pixi_hr import logger
from pixi_hr.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from pixi_hr.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from pixi_hr.pipeline.stage_03_data_transformation import DataTransformationPipeline
from pixi_hr.pipeline.stage_04_model_trainer import ModelTrainerPipeline


def main():
    """
    Main execution method for the data processing and training pipelines.

    This method sequentially:
    1. Executes the data ingestion pipeline.
    2. Executes the data validation pipeline.
    3. Executes the data transformation pipeline.

    Each pipeline has its own logging and error handling. If any pipeline fails,
    the error will be logged, and the entire program will terminate.
    """

    # List of pipeline stages to be executed in sequence
    execution_sequence = [DataIngestionTrainingPipeline(), DataValidationTrainingPipeline(), DataTransformationPipeline(), ModelTrainerPipeline()]

    for pipeline in execution_sequence:
        try:
            # Start and log the current pipeline stage
            logger.info(f">>>>>> Stage: {pipeline.STAGE_NAME} started <<<<<<")
            pipeline.main()  # consistent method name across pipelines for execution
            logger.info(f">>>>>> Stage {pipeline.STAGE_NAME} completed <<<<<< \n\nx==========x")
        except Exception as e:
            # Log any errors encountered during the pipeline's execution
            logger.exception(f"Error encountered during the {pipeline.STAGE_NAME}: {e}")
            logger.error("Program terminated due to an error.")
            exit(1)

if __name__ == "__main__":
    main()
