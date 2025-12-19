import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy import stats

def load_data(file_path):
    return pd.read_csv(file_path)

def drop_non_important(df):
    df = df.drop(columns=['Loan_ID'])
    return df

def handle_missing_values(df):
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    num_cols = df.select_dtypes(exclude=['object']).columns.tolist()
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    for col in cat_cols:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])

    print(num_cols)
    print(cat_cols)
    return df

def handle_outliers(df, column_name):
    z_scores = np.abs(stats.zscore(df[column_name].dropna()))
    df[column_name] = df[column_name][z_scores < 3] 
    return df

def handle_dependents(df):
    df['Dependents'] = df['Dependents'].replace('3+', '3')
    return df

def transform_status(df):
    df['Loan_Status'] = df['Loan_Status'].replace('Y','1')
    df['Loan_Status'] = df['Loan_Status'].replace('N','0')
    return df

def save_processed_data(df, output_path):
    df.to_csv(output_path, index=False)

if __name__ == "__main__":

    df = load_data('src/data/raw/loan.csv')

    df = drop_non_important(df)

    df = handle_missing_values(df)

    df = handle_outliers(df, 'LoanAmount')

    df = handle_dependents(df)

    df = transform_status(df)

    print(df.head())

    save_processed_data(df, 'src/data/processed/final.csv')
