import pandas as pd
from ..features.build_features import build_pipeline
from ..features.feature_selector import select_features

data_path = 'src/data/processed/final.csv' 

X_train, X_test, y_train, y_test, feature_names = build_pipeline(data_path)

feature_ranks = select_features(X_train, y_train, feature_names)

print(feature_ranks.head(5))
