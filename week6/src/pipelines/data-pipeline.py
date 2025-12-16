import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

# Load the dataset
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

# Clean the dataset
def clean_data(df):
    # Handle missing values
    imputer = SimpleImputer(strategy='mean')  # Using mean imputation for simplicity
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    
    # Remove duplicates
    df = df.drop_duplicates()

    # Outlier detection using Z-score
    z_scores = np.abs(stats.zscore(df.select_dtypes(include=np.number)))
    df = df[(z_scores < 3).all(axis=1)]  # Remove rows with Z-scores > 3
    
    # Normalize the dataset
    scaler = StandardScaler()  # You can also use MinMaxScaler based on the requirement
    df[df.select_dtypes(include=np.number).columns] = scaler.fit_transform(df.select_dtypes(include=np.number))
    
    return df

# Split the dataset into train, validation, and test sets
def split_data(df):
    X = df.drop(columns=['GII VALUE', 'HDI rank', 'Country', 'GII RANK'])
    y = df['GII VALUE']
    
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    return X_train, X_val, X_test, y_train, y_val, y_test

# Apply SMOTE if there's class imbalance
def apply_smote(X_train, y_train):
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    return X_train_res, y_train_res

# Save the processed data
def save_processed_data(df, output_filepath):
    df.to_csv(output_filepath, index=False)

# Generate an EDA report
def generate_eda_report(df):
    # Correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.savefig('/notebooks/EDA/eda_correlation_matrix.png')

    # Feature distributions
    df.select_dtypes(include=np.number).hist(bins=15, figsize=(15, 10))
    plt.savefig('/notebooks/EDA/eda_feature_distributions.png')

    # Target distribution
    plt.figure(figsize=(8, 6))
    sns.histplot(df['GII VALUE'], kde=True, color='blue')
    plt.title('Distribution of GII VALUE')
    plt.savefig('/notebooks/EDA/eda_target_distribution.png')

    # Missing values heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title('Missing Values Heatmap')
    plt.savefig('/notebooks/EDA/eda_missing_values.png')

# Full pipeline
def run_pipeline(raw_data_path, processed_data_path):
    # Step 1: Load data
    df = load_data(raw_data_path)

    # Step 2: Clean data
    df_cleaned = clean_data(df)

    # Step 3: Save cleaned data
    save_processed_data(df_cleaned, processed_data_path)

    # Step 4: Generate EDA report
    generate_eda_report(df_cleaned)
