from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    # Use modelo local finetuned por padrão
    USE_LOCAL_LLM: bool = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"
    LOCAL_MODEL_PATH: str = os.getenv("LOCAL_MODEL_PATH", "models/finetuned")

    # Fallback OpenAI (opcional)
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # RAG
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "data/processed/chroma")

    # Logging
    LOG_PATH: str = os.getenv("LOG_PATH", "logs/app.log")

settings = Settings()