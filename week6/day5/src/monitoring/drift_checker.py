import pandas as pd
import numpy as np
import joblib
from scipy.stats import ks_2samp
import src.utils.drift_logger as logger

log = logger.setup_logger()

try:
    model = joblib.load('src/models/final_finetuned_model.pkl')
    scaler = joblib.load('src/models/scaler.pkl')
    x_train = pd.read_csv('src/data/processed/X_train.csv')
    logs = pd.read_csv('prediction_logs.csv')
    log.info("All model assets and logs loaded successfully.")
except Exception as e:
    log.error(f"Failed to load assets: {e}")
    exit()

def monitor():
    log.info("Starting monitoring process...")
    
    df = logs.copy()
    dep_map = {"0":0, "1":1, "2":2, "3+":3}
    df['Dependents'] = df['Dependents'].astype(str).map(dep_map).fillna(0)
    df['Property_Area_Semiurban'] = (df['Property_Area_Semiurban'] == 'Semiurban').astype(float)
    df['Income_Ratio'] = df['ApplicantIncome'] / (df['CoapplicantIncome'] + 1)
    df['Loan_Per_Term'] = df['LoanAmount'] / (df['Loan_Amount_Term'] + 1)
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']

    scaled_feats = scaler.transform(df[scaler.feature_names_in_])
    df_scaled = pd.DataFrame(scaled_feats, columns=scaler.feature_names_in_)
    df_final = pd.concat([df_scaled, df.drop(columns=scaler.feature_names_in_, errors='ignore')], axis=1)
    X_new = df_final[model.feature_names_in_]

    for col in x_train.columns:
        _, p = ks_2samp(x_train[col], X_new[col])
        if p > 0.05:
            log.info(f"Feature '{col}': OK (p={p:.4f})")
        else:
            log.warning(f"DRIFT: Feature '{col}' (p={p:.4f})")

    acc = np.mean(model.predict(X_new) == logs['prediction'])
    log.info(f"Model Accuracy vs Logs: {acc:.2%}")
    
    if acc < 0.85:
        log.error(f"PERFORMANCE ALERT: Accuracy ({acc:.2%}) is below threshold!")

if __name__ == "__main__":
    monitor()