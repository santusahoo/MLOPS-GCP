import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.bucket_file_name = self.config['bucket_file_name']
        self.train_test_ratio = self.config['train_ratio']
        
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"data ingestion started with {self.bucket_name} and file {self.bucket_file_name}")

    def download_csv_from_gcp(self):
        """Downloads CSV file from GCP bucket."""
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Downloaded {self.bucket_file_name} from bucket {self.bucket_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error downloading file from GCP: {e}")
            raise CustomException("Error downloading file from GCP", e)
        
    def split_data(self):
        """Splits the raw data into training and testing sets."""
        try:
            logger.info("Starting data split into train and test sets")
            df = pd.read_csv(RAW_FILE_PATH)
            train_df, test_df = train_test_split(df, train_size=self.train_test_ratio, random_state=42)
            
            train_df.to_csv(TRAIN_FILE_PATH)
            test_df.to_csv(TEST_FILE_PATH)
            
            logger.info(f"Data split into train and test sets with ratio {self.train_test_ratio}")
            logger.info(f"Training data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Testing data saved to {TEST_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException("Error splitting data", e)
            
    def run(self):
        """Initiates the data ingestion process."""
        try:
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion completed successfully")
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise CustomException("Data ingestion failed", e)
        
def main():
    try:
        config = read_yaml(CONFIG_PATH)
        data_ingestion = DataIngestion(config)
        data_ingestion.run()
    except Exception as e:
        logger.error(f"Failed to run data ingestion: {e}")
        raise CustomException("Failed to run data ingestion", e)
    
if __name__ == "__main__":
    main()