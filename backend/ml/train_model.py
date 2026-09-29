"""
Model Training & Evaluation Script
Trains and compares:
1. Logistic Regression
2. Random Forest
3. XGBoost

Saves XGBoost as primary model, Random Forest as fallback, and exports comparative evaluation metrics.
"""

import json
from pathlib import Path
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier

from backend.config import settings
from backend.utils.data_generator import generate_synthetic_dataset
from backend.services.preprocessing_service import PreprocessingService


def train_and_evaluate_all():
    print(f"[*] Checking dataset at {settings.DATASET_PATH}...")
    if not settings.DATASET_PATH.exists():
        print("[-] Dataset not found. Generating synthetic dataset (1500 records)...")
        df = generate_synthetic_dataset(n_samples=1500, random_seed=42, output_path=settings.DATASET_PATH)
    else:
        import pandas as pd
        df = pd.read_csv(settings.DATASET_PATH)
        print(f"[+] Loaded existing dataset with {len(df)} records.")

    preprocessor = PreprocessingService(scaler_path=settings.SCALER_PATH)
    X_train, X_test, y_train, y_test, feature_names = preprocessor.prepare_training_data(df)

    print(f"[+] Data preprocessed. Training shape: {X_train.shape}, Testing shape: {X_test.shape}")
    print(f"[+] Total features (including engineered): {len(feature_names)}")

    # 1. Logistic Regression
    print("\n[1/3] Training Logistic Regression baseline...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    lr_probs = lr_model.predict_proba(X_test)[:, 1]

    # 2. Random Forest
    print("[2/3] Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    rf_probs = rf_model.predict_proba(X_test)[:, 1]

    # 3. XGBoost
    print("[3/3] Training XGBoost Classifier (Primary Model)...")
    xgb_model = XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=42,
        eval_metric="logloss"
    )
    xgb_model.fit(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)
    xgb_probs = xgb_model.predict_proba(X_test)[:, 1]

    def compute_metrics(y_true, y_pred, y_prob):
        return {
            "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
            "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_true, y_prob)), 4)
        }

    metrics_comparison = {
        "dataset_records": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "feature_count": len(feature_names),
        "features": feature_names,
        "models": {
            "logistic_regression": compute_metrics(y_test, lr_preds, lr_probs),
            "random_forest": compute_metrics(y_test, rf_preds, rf_probs),
            "xgboost": compute_metrics(y_test, xgb_preds, xgb_probs)
        },
        "primary_model": "xgboost",
        "fallback_model": "random_forest"
    }

    # Save artifacts
    print(f"\n[+] Saving primary XGBoost model to {settings.XGB_MODEL_PATH}...")
    settings.XGB_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(xgb_model, settings.XGB_MODEL_PATH)

    print(f"[+] Saving fallback Random Forest model to {settings.RF_MODEL_PATH}...")
    joblib.dump(rf_model, settings.RF_MODEL_PATH)

    print(f"[+] Saving model metrics comparison to {settings.METRICS_PATH}...")
    with open(settings.METRICS_PATH, "w") as f:
        json.dump(metrics_comparison, f, indent=2)

    print("\n--- MODEL PERFORMANCE COMPARISON ---")
    for name, m in metrics_comparison["models"].items():
        print(f"{name.upper():<22} | Acc: {m['accuracy']:.4f} | Prec: {m['precision']:.4f} | Rec: {m['recall']:.4f} | F1: {m['f1_score']:.4f} | AUC: {m['roc_auc']:.4f}")

    return metrics_comparison


if __name__ == "__main__":
    train_and_evaluate_all()
