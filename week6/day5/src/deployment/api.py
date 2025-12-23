import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime

app = FastAPI(title="ML Prediction Service", version="2.0.0")

try:
    model = joblib.load('src/models/final_finetuned_model.pkl')
    scaler = joblib.load('src/models/scaler.pkl')
    print(model.feature_names_in_)
    print(scaler.feature_names_in_)
except Exception as e:
    print(f"Error loading model assets: {e}")

# Request model
class PredictRequest(BaseModel):
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Dependents: str
    Total_Income: float
    Loan_Per_Term: float
    Property_Area_Semiurban: str
    Credit_History: float
    Income_Ratio: float
    Loan_Amount_Term: float

    model_config = ConfigDict(extra='ignore')

@app.post("/predict")
def predict(payload: PredictRequest):
    request_id = str(uuid.uuid4())  
    try:

        raw_df = pd.DataFrame([payload.model_dump()])
        
        # The features are organized and standardized to match the format used during model training. 
        dep_map = {"0": 0.0, "1": 1.0, "2": 2.0, "3+": 3.0}
        raw_df['Dependents'] = raw_df['Dependents'].map(dep_map).fillna(0.0)
        raw_df['Property_Area_Semiurban'] = (raw_df['Property_Area_Semiurban'] == 'Semiurban').astype(float)
        
        raw_df['Income_Ratio'] = raw_df['ApplicantIncome'] / (raw_df['CoapplicantIncome'] + 1)
        raw_df['Loan_Per_Term'] = raw_df['LoanAmount'] / (raw_df['Loan_Amount_Term'] + 1)
        raw_df['Total_Income'] = raw_df['ApplicantIncome'] + raw_df['CoapplicantIncome']

        df_aligned = raw_df
        
        scaled_features = scaler.feature_names_in_
        non_scaled_columns = [col for col in df_aligned.columns if col not in scaled_features]
        
        # the scaler omitts the feature on which it was not fitted sp we addd those fetaures again 
        scaled_values = scaler.transform(df_aligned[scaled_features])
        df_scaled = pd.DataFrame(scaled_values, columns=scaled_features)
        df_final = pd.concat([df_scaled, df_aligned[non_scaled_columns].reset_index(drop=True)], axis=1)
        
        # reordering as per training features order
        df_final = df_final[model.feature_names_in_]
        
        prediction = model.predict(df_final)
        
        log_prediction(request_id, raw_df, prediction)
        
        return {"request_id": request_id, "prediction": prediction.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

def log_prediction(request_id, input_data, prediction):

    log_data = input_data.copy()
    log_data["request_id"] = request_id
    log_data["prediction"] = prediction[0]
    log_data["timestamp"] = datetime.now().isoformat()
    log_data.to_csv('prediction_logs.csv', mode='a', header=not os.path.exists('prediction_logs.csv'),index=False)

