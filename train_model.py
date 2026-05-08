import pandas as pd
import numpy as np
import os
import joblib
import requests
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, classification_report

# 1. Download/Load Dataset
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
DATASET_PATH = "dataset/heart_disease.csv"

def download_data():
    if not os.path.exists(DATASET_PATH):
        print("Downloading dataset...")
        response = requests.get(DATA_URL)
        with open(DATASET_PATH, 'wb') as f:
            f.write(response.content)
        print("Dataset downloaded.")

def load_and_preprocess():
    # Columns for Cleveland dataset
    columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]
    
    df = pd.read_csv(DATASET_PATH, names=columns, na_values='?')
    
    # Handling missing values
    df = df.fillna(df.median())
    
    # Binary Classification (0: No disease, 1-4: Disease)
    df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0)
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    return X, y

def train_models(X, y):
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    models = {
        'Logistic Regression': LogisticRegression(),
        'Random Forest': RandomForestClassifier(n_estimators=100),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        'Decision Tree': DecisionTreeClassifier()
    }
    
    best_model = None
    best_accuracy = 0
    results = {}
    
    print("\nModel Accuracy Comparison:")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        results[name] = acc
        print(f"{name}: {acc:.4f}")
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model = model
            best_model_name = name

    print(f"\nBest Model: {best_model_name} with Accuracy: {best_accuracy:.4f}")
    
    # Save model and scaler
    joblib.dump(best_model, 'model/model.pkl')
    joblib.dump(scaler, 'model/scaler.pkl')
    
    # Also save to backend if it exists (for Docker)
    backend_model_dir = os.path.join('backend', 'model')
    if os.path.exists('backend'):
        if not os.path.exists(backend_model_dir):
            os.makedirs(backend_model_dir)
        joblib.dump(best_model, os.path.join(backend_model_dir, 'model.pkl'))
        joblib.dump(scaler, os.path.join(backend_model_dir, 'scaler.pkl'))
        print("\nModel and Scaler saved to root and backend successfully.")
    else:
        print("\nModel and Scaler saved successfully.")
    
    # Feature Importance (for Random Forest or XGBoost)
    if hasattr(best_model, 'feature_importances_'):
        importances = best_model.feature_importances_
        indices = np.argsort(importances)[::-1]
        print("\nFeature Ranking:")
        for f in range(X.shape[1]):
            print(f"{f + 1}. {X.columns[indices[f]]} ({importances[indices[f]]:.4f})")

if __name__ == "__main__":
    download_data()
    X, y = load_and_preprocess()
    train_models(X, y)
