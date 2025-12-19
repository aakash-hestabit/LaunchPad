import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

def load_data():
    X_train = pd.read_csv('src/data/processed/X_train.csv')
    X_test = pd.read_csv('src/data/processed/X_test.csv')
    y_train = pd.read_csv('src/data/processed/y_train.csv').values.flatten()
    y_test = pd.read_csv('src/data/processed/y_test.csv').values.flatten()
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    models = {
        'Logistic Regression': LogisticRegression(),
        'Random Forest': RandomForestClassifier(random_state=42),
        'XGBoost': xgb.XGBClassifier(random_state=42),
        'Neural Network': MLPClassifier(
            hidden_layer_sizes=(64, 32), 
            activation='relu', 
            solver='adam', 
            max_iter=500, 
            random_state=42
        )
    }
    
    results = {}
    
    for name, model in models.items():
        
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_probs = model.predict_proba(X_test)[:, 1]
        
        results[name] = {
            'cv_auc_mean': np.mean(cv_scores),
            'cv_auc_std': np.std(cv_scores),
            'test_accuracy': accuracy_score(y_test, y_pred),
            'test_precision': precision_score(y_test, y_pred),
            'test_recall': recall_score(y_test, y_pred),
            'test_f1_score': f1_score(y_test, y_pred),
            'test_roc_auc': roc_auc_score(y_test, y_probs),
            'model_obj': model 
        }
        
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, 
                    xticklabels=['Not Approved', 'Approved'], 
                    yticklabels=['Not Approved', 'Approved'])
        plt.title(f'{name} Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.savefig(f'src/evaluation/{name}_confusion_matrix.png')
        plt.close()
    
    return results

def save_best_model(results):
    best_model_name = max(results, key=lambda x: results[x]['cv_auc_mean'])
    best_model = results[best_model_name]['model_obj']
    
    with open('src/models/best_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    return best_model_name

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_data()
    results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    for model_name, metrics in results.items():
        print(f'\n{model_name} Results:')
        print(f"  CV ROC AUC: {metrics['cv_auc_mean']:.4f} (+/- {metrics['cv_auc_std']:.4f})")
        print(f"  Test ROC AUC: {metrics['test_roc_auc']:.4f}")
        print(f"  Test F1 Score: {metrics['test_f1_score']:.4f}")
        print("-" * 30)
    
    best_model_name = save_best_model(results)
    print(f"\nBest Model: {best_model_name} saved based on CV performance.")