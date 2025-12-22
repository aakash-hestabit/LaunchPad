from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import uuid
import logging
from datetime import datetime
import os

app = FastAPI()

MODEL_PATH = os.getenv('MODEL_PATH', 'src/models/final_finetuned_model.pkl')
model = joblib.load(MODEL_PATH)

logging.basicConfig(filename='prediction_logs.csv', level=logging.INFO, 
                    format='%(asctime)s,%(message)s')

class PredictRequest(BaseModel):
    feature1: float
    feature2: float

@app.post("/predict")
async def predict(request: Request, payload: PredictRequest):
    request_id = str(uuid.uuid4())
    
    log_entry = {
        "request_id": request_id,
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload.dict(),
    }
    
    try:
        input_data = pd.DataFrame([payload.dict()])
        prediction = model.predict(input_data)[0]
        log_entry['prediction'] = prediction
        
        logging.info(f"{log_entry['timestamp']},{log_entry['request_id']},{prediction}")
        
        return {"request_id": request_id, "prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))

