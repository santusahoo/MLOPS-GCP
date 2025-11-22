import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import load_data, read_yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataPreprocessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"Created directory for preprocessed data at {self.processed_dir}")

    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing")
            
            logger.info("dropping the columns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'] , inplace=True)
            logger.info("dropping duplicates")
            df.drop_duplicates(inplace=True)

            cat_columns = self.config["data_processing"]["categorical_features"]
            num_columns = self.config["data_processing"]["numerical_features"]

            logger.info("Encoding categorical variables")
            label_encoder = LabelEncoder()
            mappings = {}
            for col in cat_columns:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}
            logger.info(f"Categorical encoding mappings: {mappings}")


            logger.info("doing skewness handling")
            skewness_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_columns].apply(lambda x: x.skew())
            
            for col in num_columns:
                if abs(skewness[col]) > skewness_threshold:
                    df[col] = np.log1p(df[col])
                    logger.info(f"Applied log transformation to {col} due to skewness of {skewness[col]}")

            logger.info("Data preprocessing completed")

        except Exception as e:
            logger.error(f"Error during data preprocessing: {e}")
            raise CustomException("Error during data preprocessing", e)
        
    def balance_data(self, df):
        try:
            logger.info("Starting data balancing using SMOTE")
            X = df.drop('booking_status', axis=1)
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_res, y_res = smote.fit_resample(X, y)

            balanced_df = pd.concat([X_res, y_res], axis=1)
            logger.info("Data balancing completed")

            return balanced_df

        except Exception as e:
            logger.error(f"Error during data balancing: {e}")
            raise CustomException("Error during data balancing", e)
        
    def feature_selection(self, df):
        try:
            logger.info("Starting feature selection step")
            X = df.drop('booking_status', axis=1)
            y = df['booking_status']

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importances = model.feature_importances_
            feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': feature_importances})

            num_of_features_to_select = self.config["data_processing"]["num_of_features_to_select"]
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            top_10_features = top_features_importance_df["feature"].head(num_of_features_to_select).values

            selected_df = df[top_10_features.tolist() + ['booking_status']]
            logger.info(f"Selected top {num_of_features_to_select} features: {top_10_features}")

            return selected_df

        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException("Error during feature selection", e)
        
    def save_data(self, df, file_path):
        try:
            logger.info(f"Saving preprocessed data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info(f"Saved preprocessed data to {file_path}")
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {e}")
            raise CustomException(f"Error saving data to {file_path}", e)
        
    def run(self):
        try:
            logger.info("Loading data from RAW directory")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            logger.info("Data loaded successfully")

            self.preprocess_data(train_df)
            self.preprocess_data(test_df)
            logger.info("Data preprocessing completed for both train and test data")

            balanced_train_df = self.balance_data(train_df)
            logger.info("Data balancing completed for training data")

            selected_train_df = self.feature_selection(balanced_train_df)
            logger.info("Feature selection completed for both train and data")

            test_df = test_df[selected_train_df.columns]
            self.save_data(selected_train_df, PREPROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PREPROCESSED_TEST_DATA_PATH)
            logger.info("Preprocessed data saved successfully")


        except Exception as e:
            logger.error(f"Error in data preprocessing pipeline: {e}")
            raise CustomException("Error in data preprocessing pipeline", e)
        

if __name__ == "__main__":
    data_preprocessor = DataPreprocessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PREPROCESSING_DIR,
        config_path=CONFIG_PATH
    )
    data_preprocessor.run()