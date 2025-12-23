import pandas as pd
import numpy as np
import pickle
import optuna
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import json

def load_data():
    X_train = pd.read_csv('src/data/processed/X_train.csv')
    X_test = pd.read_csv('src/data/processed/X_test.csv')
    y_train = pd.read_csv('src/data/processed/y_train.csv').values.flatten()
    y_test = pd.read_csv('src/data/processed/y_test.csv').values.flatten()
    return X_train, X_test, y_train, y_test

# I USED THIS CODE TO TUNE HYPERPARAMETERS FOR THE BEST MODEL ONLY THAT IS RANDOM FOREST

# def run_grid_search(X_train, y_train):

#     param_grid = {
#         'n_estimators': [100, 200],
#         'max_depth': [10, 20],
#         'min_samples_split': [2, 5]
#     }
#     grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
#     grid.fit(X_train, y_train)
#     return grid.best_estimator_, grid.best_score_

# def run_random_search(X_train, y_train):

#     param_dist = {
#         'n_estimators': np.arange(100, 500, 50),
#         'max_depth': [None, 10, 20, 30],
#         'min_samples_split': [2, 5, 10],
#         'min_samples_leaf': [1, 2, 4]
#     }
#     random_s = RandomizedSearchCV(RandomForestClassifier(random_state=42), param_dist, n_iter=15, cv=5, scoring='roc_auc', n_jobs=-1)
#     random_s.fit(X_train, y_train)
#     return random_s.best_estimator_, random_s.best_score_

# def objective(trial, X, y):
#     params = {
#         'n_estimators': trial.suggest_int('n_estimators', 50, 500),
#         'max_depth': trial.suggest_int('max_depth', 2, 32),
#         'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
#         'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
#         'bootstrap': trial.suggest_categorical('bootstrap', [True, False])
#     }
#     rf = RandomForestClassifier(**params, random_state=42)
#     # Using cross-validation inside Optuna
#     score = cross_val_score(rf, X, y, cv=3, scoring='roc_auc').mean()
#     return score

# def run_optuna(X_train, y_train):

#     study = optuna.create_study(direction='maximize')
#     study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=20)
    
#     best_rf = RandomForestClassifier(**study.best_params, random_state=42)
#     best_rf.fit(X_train, y_train)
#     return best_rf, study.best_value

# if __name__ == "__main__":

#     X_train, X_test, y_train, y_test = load_data()

#     model_grid, score_grid = run_grid_search(X_train, y_train)
#     model_random, score_random = run_random_search(X_train, y_train)
#     model_optuna, score_optuna = run_optuna(X_train, y_train)

#     # Comparing and select the best 
#     results = {
#         "Grid Search": (model_grid, score_grid),
#         "Random Search": (model_random, score_random),
#         "Optuna": (model_optuna, score_optuna)
#     }

#     best_method = max(results, key=lambda k: results[k][1])
#     final_model = results[best_method][0]

#     with open('src/models/best_tuned_rf.pkl', 'wb') as f:
#         pickle.dump(final_model, f)




######################################################################################################3

# THIS CODE APPLIES HYPERPARAMETER TUNING ON EVERY MODEL (Random ForesT, Logistic Regression, XGboost, neural networks)
# using the three methods ( Grid Search, Random Search and Optuna) and then we select the best model with best hyperparameters from here

def neural_optuna_params(trial):
    layer = trial.suggest_categorical(
        "hidden_layer_sizes",
        ["64", "64_32", "100"]
    )

    mapping = {
        "64": (64,),
        "64_32": (64, 32),
        "100": (100,)
    }

    return {
        "alpha": trial.suggest_float("alpha", 1e-5, 1e-2, log=True),
        "hidden_layer_sizes": mapping[layer]
    }


def get_model_configs():
    return {
        'Logistic Regression': {
            'model': LogisticRegression(max_iter=1000),
            'grid': {'C': [0.01, 0.1, 1, 10], 'solver': ['liblinear', 'lbfgs']},
            'optuna': lambda trial: {
                'C': trial.suggest_float('C', 1e-3, 10, log=True),
                'solver': trial.suggest_categorical('solver', ['liblinear', 'lbfgs'])
            }
        },
        'Random Forest': {
            'model': RandomForestClassifier(random_state=42),
            'grid': {'n_estimators': [100, 200], 'max_depth': [10, 20], 'min_samples_split': [2, 5]},
            'optuna': lambda trial: {
                'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                'max_depth': trial.suggest_int('max_depth', 5, 30),
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 10)
            }
        },
        'XGBoost': {
            'model': xgb.XGBClassifier( eval_metric='logloss', random_state=42),
            'grid': {'learning_rate': [0.01, 0.1], 'max_depth': [3, 6], 'n_estimators': [100, 200]},
            'optuna': lambda trial: {
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'n_estimators': trial.suggest_int('n_estimators', 50, 300)
            }
        },
        'Neural Network': {
            'model': MLPClassifier(max_iter=1000, early_stopping=True, random_state=42),
            'grid': {'alpha': [0.0001, 0.001], 'hidden_layer_sizes': [(64,), (64, 32)]},
            'optuna': neural_optuna_params
        }
    }

def run_all_tuners(config, X, y):
    results = []
    
    # Grid Search
    gs = GridSearchCV(config['model'], config['grid'], cv=5, scoring='roc_auc', n_jobs=-1)
    gs.fit(X, y)
    results.append(('Grid', gs.best_estimator_, gs.best_score_))

    # Random Search
    rs = RandomizedSearchCV(config['model'], config['grid'], n_iter=5, cv=5, scoring='roc_auc', n_jobs=-1)
    rs.fit(X, y)
    results.append(('Random', rs.best_estimator_, rs.best_score_))

    # Optuna
    def obj(trial):
        params = config['optuna'](trial)
        m = config['model'].set_params(**params)
        return cross_val_score(m, X, y, cv=5, scoring='roc_auc').mean()
    
    study = optuna.create_study(direction='maximize')
    study.optimize(obj, n_trials=10)
    best_params = config['optuna'](study.best_trial) 
    best_optuna_model = config['model'].set_params(**best_params).fit(X, y)
    results.append(('Optuna', best_optuna_model, study.best_value))

    # Pick the winner for this specific model type
    winner = max(results, key=lambda x: x[2])
    
    pd.set_option('display.max_columns', None)
    print(X.head(10))
    return winner


def run_model_tuning():

    X_train, X_test, y_train, y_test = load_data()
    
    configs = get_model_configs()
    ranks_array = {}

    for name, config in configs.items():
        best_method, best_model, best_score = run_all_tuners(config, X_train, y_train)
        ranks_array[name] = {'method': best_method, 'model': best_model, 'score': best_score}
        print(f"{name}: {best_method} (AUC: {best_score:.4f})")

    # Find the Best model
    overall_best_name = max(ranks_array, key=lambda x: ranks_array[x]['score'])
    overall_best_model = ranks_array[overall_best_name]['model']
    overall_best_score = ranks_array[overall_best_name]['score']
    best_params = ranks_array[overall_best_name]['model'].get_params()

    serializable_params = {
        k: v for k, v in best_params.items() 
        if isinstance(v, (str, int, float, bool, list, dict, tuple))
    }

    results_data = {
        "best_model_name": overall_best_name,
        "best_score": overall_best_score,
        "best_method": ranks_array[overall_best_name]['method'],
        "best_hyperparameters": serializable_params
    }

    with open('src/tuning/results.json', 'w') as f:
        json.dump(results_data, f, indent=4)
    
    print(f"\n Best MOdel {overall_best_name} using {ranks_array[overall_best_name]['method']}")

    with open('src/models/final_finetuned_model.pkl', 'wb') as f:
        pickle.dump(overall_best_model, f)

    return overall_best_name, overall_best_model   