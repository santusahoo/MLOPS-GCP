from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTrainer
from utils.common_functions import read_yaml
from config.path_config import *


if __name__ == "__main__":
    ## data ingestion
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()

    ## data preprocessing
    data_preprocessor = DataPreprocessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PREPROCESSING_DIR,
        config_path=CONFIG_PATH
    )
    data_preprocessor.run()
    
    ## model training
    model_trainer = ModelTrainer(
            train_path=PREPROCESSED_TRAIN_DATA_PATH,
            test_path=PREPROCESSED_TEST_DATA_PATH,
            model_dir=MODEL_DIR
        )
    model_trainer.run()
    