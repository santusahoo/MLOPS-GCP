import os

###################### DATA INGESTION CONFIGURATION ######################
RAW_DIR = "artifacts/raw_data"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = "config/config.yaml"

###################### DATA PREPROCESSING CONFIGURATION ######################
PREPROCESSING_DIR = "artifacts/preprocessed"
PREPROCESSED_TRAIN_DATA_PATH = os.path.join(PREPROCESSING_DIR, "preprocessed_train.csv")
PREPROCESSED_TEST_DATA_PATH = os.path.join(PREPROCESSING_DIR, "preprocessed_test.csv")

###################### MODEL TRAINING CONFIGURATION ######################
MODEL_DIR = "artifacts/model/lgbm_model.pkl"
