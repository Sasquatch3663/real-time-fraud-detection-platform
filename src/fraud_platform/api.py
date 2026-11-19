import os
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fraud_platform.data import NUMERIC

app = FastAPI(title="Real-Time Fraud Detection API", version="1.0.0")
MODEL_PATH = os.getenv("MODEL_PATH", "models/fraud_model.joblib")
_bundle = None

def get_bundle():
    global _bundle
    if _bundle is None and Path(MODEL_PATH).exists():
        _bundle = joblib.load(MODEL_PATH)
    return _bundle

class Transaction(BaseModel):
    step: float = 0
    type: str = "PAYMENT"
    amount: float = Field(ge=0)
    oldbalanceOrg: float = 0
    newbalanceOrig: float = 0
    oldbalanceDest: float = 0
    newbalanceDest: float = 0

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": get_bundle() is not None}

def make_row(tx: Transaction, columns):
    values = tx.model_dump()
    row = {name: float(values.get(name, 0)) for name in NUMERIC}
    type_col = "type_" + tx.type
    row[type_col] = 1.0
    return pd.DataFrame([{col: row.get(col, 0.0) for col in columns}], columns=columns)

@app.post("/predict")
def predict(tx: Transaction):
    bundle = get_bundle()
    if bundle is None:
        raise HTTPException(status_code=503, detail="Model not found. Train it first.")
    try:
        X = make_row(tx, bundle["feature_columns"])
        score = float(bundle["model"].predict_proba(X)[0, 1])
        threshold = float(bundle.get("threshold", 0.5))
        return {"fraud_probability": score, "is_fraud": score >= threshold, "threshold": threshold}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
