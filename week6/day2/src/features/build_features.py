import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier
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
    df['Has_Cabin'] = df['Ticket'].apply(lambda x: 1 if isinstance(x, str) and any(c.isalpha() for c in x) else 0)
    df['SibSp_Parch_Ratio'] = df['SibSp'] / (df['Parch'] + 1)
    df['FarePerPerson'] = df['Fare'] / (df['FamilySize'])
    
    df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
    df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    df['Title'] = df['Title'].replace(['Mlle', 'Ms'], 'Miss')
    df['Title'] = df['Title'].replace('Mme', 'Mrs')
    
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    return df

def select_features(X, y):

    mi = mutual_info_classif(X, y, random_state=42)
    mi_selected = X.columns[mi >= 0.05].tolist() 
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    selector = RFE(model, n_features_to_select=10)
    selector.fit(X, y)
    rfe_selected = X.columns[selector.support_].tolist()
    
    return list(set(mi_selected).union(set(rfe_selected)))

def build_pipeline(data_path):
    df = pd.read_csv(data_path)
    df = generate_features(df)
    
    X = df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Survived'])
    y = df['Survived']
    
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()
    num_cols = X.select_dtypes(exclude=['object']).columns.tolist()

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    scaler = StandardScaler()
    
    X_train_num = scaler.fit_transform(X_train_raw[num_cols])
    X_train_cat = ohe.fit_transform(X_train_raw[cat_cols])
    
    X_test_num = scaler.transform(X_test_raw[num_cols])
    X_test_cat = ohe.transform(X_test_raw[cat_cols])
    
    feat_names = num_cols + list(ohe.get_feature_names_out(cat_cols))
    X_train_processed = pd.DataFrame(np.hstack([X_train_num, X_train_cat]), columns=feat_names, index=X_train_raw.index)
    X_test_processed = pd.DataFrame(np.hstack([X_test_num, X_test_cat]), columns=feat_names, index=X_test_raw.index)

    selected_features = select_features(X_train_processed, y_train)
    
    X_train_final = X_train_processed[selected_features]
    X_test_final = X_test_processed[selected_features]

    with open('src/features/feature_list.json', 'w') as f:
        json.dump(selected_features, f)
    
    X_train_final.assign(Survived=y_train).to_csv('src/data/processed/train_final.csv', index=False)
    X_test_final.assign(Survived=y_test).to_csv('src/data/processed/test_final.csv', index=False)
    
    logger.info("Pipeline Built Successfully with %d features", len(selected_features))
    return X_train_final, X_test_final, y_train, y_test, selected_features

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, features = build_pipeline('data/processed/final.csv')