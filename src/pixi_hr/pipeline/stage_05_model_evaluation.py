from pixi_hr import logger
from pixi_hr.config.configuration import ConfigurationManager
from pixi_hr.components.model_evaluation import ModelEvaluation


class ModelEvaluationPipeline:
    """
    Pipeline class for the model evaluation phase.

    This pipeline performs the following steps:
    1. Initializes the configuration manager.
    2. Fetches the model evaluation configuration.
    3. Initializes the ModelEvaluation component.
    4. Logs evaluation metrics into MLFlow.

    Attributes:
    - STAGE_NAME (str): Name of the stage (used for logging purposes).
    - config_manager (ConfigurationManager): Instance of the configuration manager.

    Methods:
    - main(): Executes the main functionality of the ModelEvaluationPipeline.
    """
    
    STAGE_NAME = "Model Evaluation Stage"

    def __init__(self):
        """
        Initializes the ModelEvaluationPipeline.
        Sets up the configuration manager.
        """
        self.config_manager = ConfigurationManager()

    def main(self):
        """
        Executes the main functionality of the ModelEvaluationPipeline.
        """
        logger.info("Starting the Model Evaluation Pipeline")

        # Fetch the model evaluation configuration
        model_evaluation_config = self.config_manager.get_model_evaluation_config()

        # Initialize the ModelEvaluation component
        model_evaluation = ModelEvaluation(config=model_evaluation_config)

        # Log the evaluation metrics into MLFlow
        model_evaluation.log_into_mlflow()

        logger.info("Model Evaluation Pipeline Completed Successfully.")


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> Stage: {ModelEvaluationPipeline.STAGE_NAME} started <<<<<<")
        model_evaluation_pipeline = ModelEvaluationPipeline()
        model_evaluation_pipeline.main()
        logger.info(f">>>>>> Stage {ModelEvaluationPipeline.STAGE_NAME} completed <<<<<< \n\nx==========x")
    except Exception as e:
        logger.exception(f"Error encountered during the {ModelEvaluationPipeline.STAGE_NAME}: {e}")
        raise
