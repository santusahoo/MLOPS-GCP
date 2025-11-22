import os
import sys
from src.logger import get_logger
import pandas as pd
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    """Reads a YAML file and returns the content as a dictionary."""
    try:
        if not os.path.exists(file_path):
            logger.error(f"The file {file_path} does not exist.")
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
        logger.info(f"YAML file {file_path} read successfully.")
        return content
    except Exception as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException(f"Error reading YAML file {file_path}", sys)
    

def load_data(file_path):
    try:
        logger.info(f"Loading data from {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"The file {file_path} does not exist.")
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        data = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise CustomException(f"Error loading data from {file_path}", sys)