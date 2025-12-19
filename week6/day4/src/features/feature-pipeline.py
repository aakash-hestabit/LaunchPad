import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import json

def load_data(file_path):
    return pd.read_csv(file_path)

def handle_missing_values(df):
    df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
    df['Self_Employed'] = df['Self_Employed'].fillna(df['Self_Employed'].mode()[0])
    df['Dependents'] = df['Dependents'].fillna(df['Dependents'].mode()[0])
    return df

def generate_new_features(df):
    df['Income_Ratio'] = df['ApplicantIncome'] / (df['CoapplicantIncome'] + 1) 
    df['Loan_Per_Term'] = df['LoanAmount'] / df['Loan_Amount_Term']
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['LoanAmount_log'] = np.log1p(df['LoanAmount']) 
    return df

def encode_categorical_features(df):
    categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    
    encoder = OneHotEncoder(sparse_output=False,handle_unknown='ignore')
    
    encoded_feat = encoder.fit_transform(df[categorical_cols])
    
    encoded_df = pd.DataFrame(
        encoded_feat, 
        columns=encoder.get_feature_names_out(categorical_cols),
        index=df.index
    )
    
    return pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)

def scale_numerical_features(df, numerical_cols):
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    return df

def remove_highly_correlated_features(df, threshold=0.9):
    corr_matrix = df.corr()
    to_drop = set()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                colname = corr_matrix.columns[i]
                to_drop.add(colname)
    df = df.drop(columns=to_drop)
    return df

def select_by_mutual_information(X, y, threshold=0.1):
    mi = mutual_info_classif(X, y)
    selected_features = X.columns[mi >= threshold]
    return selected_features

def select_by_rfe(X, y, n_features_to_select=10):
    model = RandomForestClassifier(random_state=42)
    selector = RFE(model, n_features_to_select=n_features_to_select)
    selector = selector.fit(X, y)
    selected_features = X.columns[selector.support_]
    return selected_features

def split_data(df, target_column='Loan_Status'):
    X = df.drop(columns=[target_column])
    y = df[target_column] 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

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
    
    feature_importance = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': selected_features, 'Importance': feature_importance})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=importance_df)
    plt.title("Feature Importance")
    plt.savefig('./feature_importance.png')
    plt.close()

def plot_correlation_heatmap(df):
    corr_matrix = df.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    plt.savefig('./correlation_heatmap.png')
    plt.close()

def plot_feature_distributions(df, selected_features):
    plt.figure(figsize=(12, 8))
    df[selected_features].hist(bins=20, figsize=(15, 10))
    plt.suptitle('Feature Distributions')
    plt.savefig('./feature_distributions.png')
    plt.close()

def feature_engineering_pipeline(df, target_column='Loan_Status'):
    df = handle_missing_values(df)
    
    df = generate_new_features(df)
    
    df = encode_categorical_features(df)
    
    numerical_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Income_Ratio', 'Loan_Per_Term', 'Total_Income']
    df = scale_numerical_features(df, numerical_cols)
    
    df = remove_highly_correlated_features(df)
    
    X_train, X_test, y_train, y_test = split_data(df, target_column)
    
    selected_features_mi = select_by_mutual_information(X_train, y_train, threshold=0.1)
    
    selected_features_rfe = select_by_rfe(X_train, y_train, n_features_to_select=10)
    
    selected_features_set = set(selected_features_mi).union(set(selected_features_rfe))
    selected_features = list(selected_features_set)

    save_processed_data(X_train[selected_features], X_test[selected_features], y_train, y_test, selected_features)

    plot_feature_importance(X_train, y_train, selected_features)
    plot_correlation_heatmap(df)
    plot_feature_distributions(df, selected_features)
    
    return X_train[selected_features], X_test[selected_features], y_train, y_test, selected_features

if __name__ == "__main__":

    df = load_data('src/data/processed/final.csv')
    
    X_train, X_test, y_train, y_test, selected_features = feature_engineering_pipeline(df)

    print(f"Selected Features: {selected_features}")
