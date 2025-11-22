import os
import joblib
from src.logger import get_logger
from src.custom_exception import CustomException
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgbm
from config.model_params import lightgbm_model_params, RANDOM_SEARCH_PARAMS
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from config.path_config import *
from config.model_params import *
from utils.common_functions import load_data

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)


class ModelTrainer:
    def __init__(self, train_path, test_path, model_dir):
        self.train_path = train_path
        self.test_path = test_path
        self.model_dir = model_dir

        self.params_dist = lightgbm_model_params
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info("Loading training and testing data")
            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)
            logger.info("Successfully loaded training and testing data")

            X_train = train_data.drop(columns=['booking_status'])
            y_train = train_data['booking_status']

            X_test = test_data.drop(columns=['booking_status'])
            y_test = test_data['booking_status']
            logger.info("Successfully split data into features and target")

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error loading and splitting data: {e}")
            raise CustomException("Error loading and splitting data", e)
        
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Starting LightGBM model training with RandomizedSearchCV")
            lgbm_model = lgbm.LGBMClassifier(random_state=self.random_search_params['random_state'])
            logger.info("Initialized LightGBM Classifier")
            logger.info("Performing Randomized Search for hyperparameter tuning")
            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
                )
            logger.info("Fitting RandomizedSearchCV to training data")
            random_search.fit(X_train, y_train)
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_
            logger.info("Successfully trained LightGBM model with best hyperparameters")
            logger.info(f"Best Hyperparameters: {best_params}")
            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error during LightGBM model training: {e}")
            raise CustomException("Error during LightGBM model training", e)

    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating model performance on test data")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Model Evaluation Metrics: Accuracy={accuracy}, Precision={precision}, Recall={recall}, F1-Score={f1}")

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }
        
        except Exception as e:
            logger.error(f"Error during model evaluation: {e}")
            raise CustomException("Error during model evaluation", e)
        

    def save_model(self, model):
        try:
            logger.info(f"Saving trained model to {self.model_dir}")
            os.makedirs(os.path.dirname(self.model_dir), exist_ok=True)
            joblib.dump(model, self.model_dir)
            logger.info(f"Model saved successfully at {self.model_dir}")

        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise CustomException("Error saving model", e)
        
    def run(self):
        try:
            with mlflow.start_run():

                logger.info("starting our MLflow run for model training")
                logger.info("Starting model training pipeline")
                logger.info("logging the training and testing dataset to MLflow")
                
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")


                X_train, y_train, X_test, y_test = self.load_and_split_data()
                model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(model, X_test, y_test)
                self.save_model(model)

                logger.info("Logging model and metrics to MLflow")
                mlflow.log_artifact(self.model_dir, artifact_path="model")

                mlflow.log_params(model.get_params())
                mlflow.log_metrics(metrics)

                return metrics
        
        except Exception as e:
            logger.error(f"Error in model training pipeline: {e}")
            raise CustomException("Error in model training pipeline", e)
        
if __name__ == "__main__":
    try:
        model_trainer = ModelTrainer(
            train_path=PREPROCESSED_TRAIN_DATA_PATH,
            test_path=PREPROCESSED_TEST_DATA_PATH,
            model_dir=MODEL_DIR
        )
        evaluation_metrics = model_trainer.run()
        logger.info(f"Model training pipeline completed successfully with metrics: {evaluation_metrics}")

    except Exception as e:
        logger.error(f"Failed to complete model training pipeline: {e}")
