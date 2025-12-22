python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force data\raw,data\processed,data\synthetic,models\finetuned,logs,reports | Out-Null
Write-Host "OK: ambiente criado."