import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import src.utils.logger as lowgger

logger = lowgger.setup_logger()

def generate_features(df):
    df = df.copy()
    
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    df['NameLength'] = df['Name'].apply(len)
    df['FareBin'] = pd.qcut(df['Fare'], 4, labels=False, duplicates='drop')
    df['Age_Class'] = df['Age'] * df['Pclass']
    df['IsMinor'] = (df['Age'] < 1.0).astype(int)
    df['Has_Cabin'] = df['Ticket'].apply(lambda x: 1 if isinstance(x, str) and x.isalpha() else 0)
    df['SibSp_Parch_Ratio'] = df['SibSp'] / (df['Parch'] + 1)
    df['FarePerPerson'] = df['Fare'] / (df['FamilySize'])
    
    df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
    
    df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col',\
 	'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    
    df['Title'] = df['Title'].replace('Mlle', 'Miss')
    df['Title'] = df['Title'].replace('Ms', 'Miss')
    df['Title'] = df['Title'].replace('Mme', 'Mrs')
    
    return df

def build_pipeline(data_path):
    df = pd.read_csv(data_path)
    df = generate_features(df)
    
    X = df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Survived'])
    y = df['Survived']
    
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()
    num_cols = X.select_dtypes(exclude=['object']).columns.tolist()
    
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    scaler = StandardScaler()
    
    X_train_final = np.hstack([scaler.fit_transform(X_train_raw[num_cols]), ohe.fit_transform(X_train_raw[cat_cols])])
    
    X_test_final = np.hstack([scaler.transform(X_test_raw[num_cols]), ohe.transform(X_test_raw[cat_cols])])
    
    feature_names = num_cols + list(ohe.get_feature_names_out(cat_cols))

    with open('src/features/feature_list.json', 'w') as f:
        json.dump(feature_names, f)
    
    train_df_final = pd.DataFrame(X_train_final, columns=feature_names)
    train_df_final['Survived'] = y_train.values 
    
    test_df_final = pd.DataFrame(X_test_final, columns=feature_names)
    test_df_final['Survived'] = y_test.values
    
    train_df_final.to_csv('src/data/processed/train_final.csv', index=False)
    test_df_final.to_csv('src/data/processed/test_final.csv', index=False)
    logger.info(" Pipeline Built Successfully")
    return X_train_final, X_test_final, y_train, y_test, feature_names

if __name__ == "__main__":
    X_train, y_train, features = build_pipeline('data/processed/final.csv')