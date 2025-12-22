python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp -n .env.example .env || true
mkdir -p data/raw data/processed data/synthetic models/finetuned logs reports
echo "OK: ambiente criado."