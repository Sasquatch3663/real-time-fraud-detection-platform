import argparse
from pathlib import Path
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score, accuracy_score
from xgboost import XGBClassifier
from fraud_platform.data import load_data, prepare_features

def train(data_path: str, model_path: str):
    df = load_data(data_path)
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scale_pos_weight = max(1.0, (y_train == 0).sum() / max(1, (y_train == 1).sum()))
    model = XGBClassifier(n_estimators=250, max_depth=6, learning_rate=0.08, subsample=0.85,
        colsample_bytree=0.85, objective="binary:logistic", eval_metric="auc",
        scale_pos_weight=scale_pos_weight, n_jobs=4, random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.5).astype(int)
    metrics = {"accuracy": accuracy_score(y_test, pred), "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0), "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob)}
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    bundle = {"model": model, "feature_columns": list(X.columns), "threshold": 0.5}
    joblib.dump(bundle, model_path)
    try:
        mlflow.set_tracking_uri(__import__('os').getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))
        with mlflow.start_run():
            mlflow.log_params({"model": "XGBClassifier", "n_estimators": 250, "max_depth": 6, "threshold": 0.5})
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, "model")
    except Exception as exc:
        print(f"MLflow logging skipped: {exc}")
    print("Metrics:", metrics)
    print(f"Saved model: {model_path}")
    return metrics

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/transactions.csv")
    parser.add_argument("--model", default="models/fraud_model.joblib")
    args = parser.parse_args()
    train(args.data, args.model)

if __name__ == "__main__": main()
