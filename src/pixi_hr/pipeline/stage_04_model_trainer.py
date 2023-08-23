from pixi_hr import logger
from pixi_hr.config.configuration import ConfigurationManager
from pixi_hr.components.model_trainer import ModelTrainer


class ModelTrainerPipeline:
    """
    Pipeline class for the model training phase.

    This pipeline performs the following steps:
    1. Initializes configuration management.
    2. Fetches the model training configuration.
    3. Initializes the ModelTrainer component.
    4. Trains the model using the training data.

    Attributes:
    - STAGE_NAME (str): Name of the stage (used for logging purposes).
    - config (ConfigurationManager): Instance of the ConfigurationManager.
    
    Methods:
    - main(): Executes the main functionality of the ModelTrainerPipeline.
    """
    
    STAGE_NAME = "Model Training Stage"

    def __init__(self):
        """
        Initializes the ModelTrainerPipeline.
        Sets up the configuration manager.
        """
        # Step 1: Initialize Configuration Manager
        self.config_manager = ConfigurationManager()

    def main(self):
        """
        Executes the main functionality of the ModelTrainerPipeline.
        """
        logger.info("Starting the Model Training Pipeline")

        # Step 2: Fetch Model Training Configuration
        model_trainer_config = self.config_manager.get_model_trainer_config()

        # Step 3: Initialize Model Trainer Component
        model_trainer = ModelTrainer(config=model_trainer_config)

        # Step 4: Train Model
        model_trainer.main()

        logger.info("Model Training Pipeline Completed Successfully.")

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> Stage: {ModelTrainerPipeline.STAGE_NAME} started <<<<<<")
        model_trainer_pipeline = ModelTrainerPipeline()
        model_trainer_pipeline.main()
        logger.info(f">>>>>> Stage {ModelTrainerPipeline.STAGE_NAME} completed <<<<<< \n\nx==========x")
    except Exception as e:
        logger.exception(f"Error encountered during the {ModelTrainerPipeline.STAGE_NAME}: {e}")
        raise
