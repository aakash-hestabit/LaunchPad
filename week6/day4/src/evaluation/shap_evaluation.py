import shap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
import os

def load_data():
    """Loads processed datasets from the project directory."""
    X_train = pd.read_csv('src/data/processed/X_train.csv')
    X_test = pd.read_csv('src/data/processed/X_test.csv')
    y_train = pd.read_csv('src/data/processed/y_train.csv').values.flatten()
    y_test = pd.read_csv('src/data/processed/y_test.csv').values.flatten()
    return X_train, X_test, y_train, y_test

def run_evaluation(overall_best_name, overall_best_model):
    
    X_train, X_test, y_train, y_test = load_data()
    y_pred = overall_best_model.predict(X_test)

    # Bias/Variance Analysis 
    train_acc = overall_best_model.score(X_train, y_train)
    test_acc = overall_best_model.score(X_test, y_test)
    
    plt.figure(figsize=(6, 4))
    plt.bar(['Train Accuracy', 'Test Accuracy'], [train_acc, test_acc], color=['#3498db', '#e74c3c'])
    plt.ylim(0, 1.1)
    plt.title(f'Bias/Variance Check: {overall_best_name}')
    for i, v in enumerate([train_acc, test_acc]):
        plt.text(i, v + 0.02, f'{v:.2f}', ha='center', fontweight='bold')
    plt.savefig('src/evaluation/bias_variance.png')
    plt.close()

    # Error Clustering
    pca = PCA(n_components=2)
    X_embedded = pca.fit_transform(X_test)
    
    df_viz = pd.DataFrame(X_embedded, columns=['PC1', 'PC2'])
    df_viz['Actual'] = y_test
    df_viz['Predicted'] = y_pred
    df_viz['Status'] = np.where(df_viz['Actual'] == df_viz['Predicted'], 'Correct', 'Error')

    

    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=df_viz, 
        x='PC1', y='PC2', 
        hue='Status', 
        palette={'Correct': '#bdc3c7', 'Error': '#e74c3c'},
        alpha=0.7,
        style='Status',
        markers={'Correct': 'o', 'Error': 'X'}
    )
    plt.title(f"Error Clustering (PCA Projection): {overall_best_name}")
    plt.savefig('src/evaluation/error_clusters.png')
    plt.close()

    # Sampling for speed as shap can be slow on large test sets
    X_sample = X_test.sample(min(100, len(X_test)), random_state=42)
    
    try:
        explainer = shap.TreeExplainer(overall_best_model)

        shap_values = explainer(X_sample)

        plt.figure(figsize=(12, 8))
        if len(shap_values.shape) == 3: 
            shap.summary_plot(shap_values[:, :, 1], X_sample, show=False)
        else:
            shap.summary_plot(shap_values, X_sample, show=False)
            
        plt.title(f"SHAP Summary Plot: {overall_best_name}")
        plt.savefig('src/evaluation/shap_summary.png', bbox_inches='tight')
        plt.close()


        plt.figure(figsize=(12, 8))
        if len(shap_values.shape) == 3:
            shap.plots.bar(shap_values[:, :, 1], show=False)
        else:
            shap.plots.bar(shap_values, show=False)
            
        plt.title(f"Feature Importance (SHAP): {overall_best_name}")
        plt.savefig('src/evaluation/feature_importance.png', bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        print(f"SHAP evaluation failed: {e}")



    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=['Predicted 0', 'Predicted 1'],
        yticklabels=['Actual 0', 'Actual 1']
    )
    plt.title(f"Confusion Matrix: {overall_best_name}")
    plt.ylabel('Actual Label')
    plt.xlabel('Predicted Label')
    plt.savefig('src/evaluation/error_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("shap analysis complete")