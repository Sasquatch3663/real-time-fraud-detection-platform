from pathlib import Path
import pandas as pd

TARGET = "isFraud"
NUMERIC = ["step", "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]

def load_data(path: str) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}. Place PaySim CSV there.")
    df = pd.read_csv(path)
    if TARGET not in df.columns:
        raise ValueError(f"Dataset must contain target column '{TARGET}'.")
    return df

def prepare_features(df: pd.DataFrame):
    missing = [c for c in NUMERIC if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required PaySim columns: {missing}")
    features = df[NUMERIC].copy()
    if "type" in df.columns:
        encoded = pd.get_dummies(df["type"].astype(str), prefix="type")
        features = pd.concat([features, encoded], axis=1)
    features = features.fillna(0)
    return features.astype(float), df[TARGET].astype(int)
