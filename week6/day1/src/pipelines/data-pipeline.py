import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import utils.logger as lowgger

logger = lowgger.setup_logger()

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        logger.info("Dataset Loaded")
        return df
    except FileNotFoundError:
        logger.error(f"File not found at {filepath}")
        return pd.DataFrame()

def clean_data(df):
    try:
        df = df.drop_duplicates()  
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')] 
        df = df.dropna(axis=1, how='all')
        df['Age'].fillna(df['Age'].median(), inplace=True)
        df['Fare'].fillna(df['Fare'].median(), inplace=True)

        if 'Cabin' in df.columns:
            df.drop('Cabin', axis=1, inplace=True)

        df.dropna(inplace=True)

        for col in ['Age', 'Fare']:
            Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            df[col] = np.clip(df[col], lower, upper)

        scaler = StandardScaler()
        df[['Age', 'Fare']] = scaler.fit_transform(df[['Age', 'Fare']])
        logger.info("Dataset Cleaned")
        return df
    except Exception as e:
        logger.error("Error while cleaning data",e)
        return pd.DataFrame()


def save_processed_data(df, output_filepath):
    try:
        df.to_csv(output_filepath, index=False)
        logger.info("Cleaned Dataset saved")
    except Exception as e:
        logger.error("Error while saving cleaned dataset",e)
        return pd.DataFrame()

def run_pipeline(raw_data_path, processed_data_path):
    df = load_data(raw_data_path)
    if df.empty:
        return

    df = clean_data(df)
    save_processed_data(df, processed_data_path)

if __name__ == "__main__":
    run_pipeline("src/data/raw/tested.csv", "src/data/processed/final.csv")
