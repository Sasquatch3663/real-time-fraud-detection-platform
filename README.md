# Real-Time Financial Fraud Detection Platform

A deployable starter platform for PaySim-style transaction fraud detection. It includes data preparation, XGBoost training with MLflow tracking, FastAPI inference, Kafka event publishing/consumption, Streamlit dashboard, drift-report generation, Feast feature definitions, Docker Compose, Kubernetes manifests, and tests.

## 1. Dataset

Download the PaySim CSV separately (commonly named `PS_20174392719_1491204439457_log.csv`) and place it at `data/raw/transactions.csv`. The expected target is `isFraud`. The pipeline supports the standard PaySim columns. Do not commit the dataset.

## 2. Run locally on Windows PowerShell

Install Python 3.11 and Docker Desktop. From the extracted project directory:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .[test]
python -m fraud_platform.train --data data/raw/transactions.csv
pytest
```

Start the stack (API, dashboard, Kafka, MLflow):

```powershell
docker compose up --build -d
```

Open API docs at http://localhost:8000/docs, dashboard at http://localhost:8501, MLflow at http://localhost:5000. Check health: `http://localhost:8000/health`.

Send a sample prediction (PowerShell):

```powershell
$body = @{step=1; type='TRANSFER'; amount=9000; oldbalanceOrg=10000; newbalanceOrig=1000; oldbalanceDest=0; newbalanceDest=9000} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8000/predict -ContentType 'application/json' -Body $body
```

Publish a transaction to Kafka (after stack is up):

```powershell
python -m fraud_platform.producer --bootstrap localhost:9092 --count 10
```

Consume and score Kafka messages in a separate terminal:

```powershell
python -m fraud_platform.consumer --bootstrap localhost:9092
```

## 3. Monitoring and graph model

Generate a drift report comparing two CSVs (reference and current):
`python -m fraud_platform.monitor --reference data/processed/reference.csv --current data/processed/current.csv`

Optional graph model dependencies: `pip install -e .[graph]`. Run `python -m fraud_platform.graph_train --data data/raw/transactions.csv`. This is a simple transaction similarity graph baseline; it is separate from the production API model, which uses XGBoost.

## 4. Feast

The feature repo is in `feature_repo/`. From that directory run `feast apply`. The included file uses a local SQLite registry and file-based offline/online stores for development. Configure a production online store before deployment.

## 5. Kubernetes

Build and push the image to your registry, update `k8s/deployment.yaml` image name, and apply:
`kubectl apply -f k8s/`

Kubernetes manifests deploy the API and dashboard. Kafka/MLflow are intentionally externalized for production; use managed services or deploy them with their supported operators/charts. Mount a trained model at `/app/models/fraud_model.joblib` and configure secrets/networking for your environment.

## 6. Important deployment notes

- Train the model before starting API inference; model file is created at `models/fraud_model.joblib`.
- PaySim is highly imbalanced. Review precision/recall and tune the threshold for your business costs; the default threshold is 0.5.
- Do not use this demo as the sole control for real financial transactions without security, privacy, load, model validation, and human-review controls.
