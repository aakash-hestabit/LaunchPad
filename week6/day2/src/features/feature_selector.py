import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import src.utils.logger as logger

logger = logger.setup_logger()

def select_features(X, y, feature_names):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    importances = model.feature_importances_
    feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feat_imp.values[:15], y=feat_imp.index[:15])
    plt.title("Top 15 Feature Importances")
    plt.savefig('feature_importance.png')
    logger.info("Feature importance plotted")
    
    return feat_imp