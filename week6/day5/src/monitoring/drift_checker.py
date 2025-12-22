import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
import joblib
import os
import logging

REFERENCE_DATA_PATH = os.getenv('REFERENCE_DATA_PATH', 'data/reference_data.csv')
reference_data = pd.read_csv(REFERENCE_DATA_PATH)

MODEL_PATH = os.getenv('MODEL_PATH', 'src/models/final_finetuned_model.pkl')
model = joblib.load(MODEL_PATH)


def check_data_drift(new_data: pd.DataFrame):
    
    
    mae = mean_absolute_error(reference_data, new_data)
    if mae > 0.1:  
        logging.warning(f"Data drift detected with MAE: {mae}")
        return True
    return False

def log_accuracy_decay(new_data: pd.DataFrame, actual_labels: np.array):
    
    predictions = model.predict(new_data)
    accuracy = np.mean(predictions == actual_labels)
    if accuracy < 0.85:  
        logging.warning(f"Accuracy decay detected. Current accuracy: {accuracy}")
        return True
    return False

