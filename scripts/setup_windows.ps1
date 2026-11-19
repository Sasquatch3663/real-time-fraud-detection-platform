$ErrorActionPreference = 'Stop'
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install -e .[test]
New-Item -ItemType Directory -Force data/raw,data/processed,models,reports | Out-Null
Write-Host 'Setup complete. Place PaySim CSV at data/raw/transactions.csv.'
