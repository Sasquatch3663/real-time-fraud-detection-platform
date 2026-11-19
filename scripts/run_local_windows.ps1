$ErrorActionPreference = 'Stop'
if (!(Test-Path '.venv\Scripts\python.exe')) { throw 'Run scripts/setup_windows.ps1 first.' }
.\.venv\Scripts\python.exe -m fraud_platform.train --data data/raw/transactions.csv
.\.venv\Scripts\python.exe -m uvicorn fraud_platform.api:app --host 127.0.0.1 --port 8000
