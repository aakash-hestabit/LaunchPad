import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import joblib

def load_data(file_path):
    return pd.read_csv(file_path)

def handle_missing_values(df):
    df = df.copy()
    df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
    df['Self_Employed'] = df['Self_Employed'].fillna(df['Self_Employed'].mode()[0])
    df['Dependents'] = df['Dependents'].fillna(df['Dependents'].mode()[0])
    if 'Credit_History' in df.columns:
        df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mode()[0])
    return df

def generate_new_features(df):
    df = df.copy()
    df['Income_Ratio'] = df['ApplicantIncome'] / (df['CoapplicantIncome'] + 1) 
    df['Loan_Per_Term'] = df['LoanAmount'] / (df['Loan_Amount_Term'] + 1)
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['LoanAmount_log'] = np.log1p(df['LoanAmount']) 
    return df

def clean_dataframe(df):
    df = df.copy()
    if 'Loan_ID' in df.columns:
        df = df.drop(columns=['Loan_ID'])
    if df['Loan_Status'].dtype == 'O':
        le = LabelEncoder()
        df['Loan_Status'] = le.fit_transform(df['Loan_Status'])
    return df

def save_processed_data(X_train, X_test, y_train, y_test, selected_features):
    X_train.to_csv('src/data/processed/X_train.csv', index=False)
    X_test.to_csv('src/data/processed/X_test.csv', index=False)
    y_train.to_csv('src/data/processed/y_train.csv', index=False)
    y_test.to_csv('src/data/processed/y_test.csv', index=False)
    with open('./feature_list.json', 'w') as f:
        json.dump(list(selected_features), f)

def plot_feature_importance(X, y, selected_features):
    model = RandomForestClassifier(random_state=42)
    model.fit(X[selected_features], y)
    importance_df = pd.DataFrame({'Feature': selected_features, 'Importance': model.feature_importances_})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=importance_df)
    plt.title("Feature Importance")
    plt.savefig('./feature_importance.png')
    plt.close()

def feature_engineering_pipeline(df, target_column='Loan_Status'):
    df = handle_missing_values(df)
    df = generate_new_features(df)
    df = clean_dataframe(df)
    
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    
    encoded_train = encoder.fit_transform(X_train[categorical_cols])
    encoded_train_df = pd.DataFrame(encoded_train, columns=encoder.get_feature_names_out(), index=X_train.index)
    encoded_test = encoder.transform(X_test[categorical_cols])
    encoded_test_df = pd.DataFrame(encoded_test, columns=encoder.get_feature_names_out(), index=X_test.index)
    
    X_train = pd.concat([X_train.drop(columns=categorical_cols), encoded_train_df], axis=1)
    X_test = pd.concat([X_test.drop(columns=categorical_cols), encoded_test_df], axis=1)

    num_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 
                'Income_Ratio', 'Loan_Per_Term', 'Total_Income', 'LoanAmount_log']
    scaler = StandardScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    mi = mutual_info_classif(X_train, y_train)
    mi_selected = X_train.columns[mi > 0.01]

    rfe_selector = RFE(RandomForestClassifier(n_estimators=50, random_state=42), n_features_to_select=10)
    rfe_selector.fit(X_train, y_train)
    rfe_selected = X_train.columns[rfe_selector.support_]

    selected_features = list(set(mi_selected) | set(rfe_selected))

    os.makedirs('src/data/processed', exist_ok=True)
    save_processed_data(X_train[selected_features], X_test[selected_features], y_train, y_test, selected_features)
    plot_feature_importance(X_train, y_train, selected_features)

    joblib.dump(encoder, 'src/models/encoder.pkl')
    
    joblib.dump(scaler, 'src/models/scaler.pkl')

    joblib.dump(selected_features, 'src/models/selected_features.pkl')
    
    return X_train[selected_features], X_test[selected_features], y_train, y_test, selected_features

if __name__ == "__main__":
    df = load_data('src/data/processed/final.csv')
    X_train, X_test, y_train, y_test, selected_features = feature_engineering_pipeline(df)
    print(f"Selected Features: {selected_features}")