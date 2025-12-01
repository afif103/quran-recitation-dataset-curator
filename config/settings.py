from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    huggingface_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    cerebras_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None
    kaggle_api_key: Optional[str] = None
    log_level: str = "INFO"
    data_dir: str = "data"
    backup_dir: str = "data/backup"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    s3_bucket_name: Optional[str] = None
    cerebras_model: str = "llama-3.1-8b-instant"

    model_config = {
        "env_file": "config/.env",
        "env_file_encoding": "utf-8",
    }


def get_settings():
    # Try to load from Streamlit secrets if available
    try:
        import streamlit as st

        if hasattr(st, "secrets") and st.secrets:
            return Settings(
                huggingface_api_key=st.secrets.get("HUGGINGFACE_API_KEY"),
                groq_api_key=st.secrets.get("GROQ_API_KEY"),
                cerebras_api_key=st.secrets.get("CEREBRAS_API_KEY"),
                langsmith_api_key=st.secrets.get("LANGSMITH_API_KEY"),
                kaggle_api_key=st.secrets.get("KAGGLE_API_KEY"),
                aws_access_key_id=st.secrets.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=st.secrets.get("AWS_SECRET_ACCESS_KEY"),
                s3_bucket_name=st.secrets.get("S3_BUCKET_NAME"),
            )
    except (ImportError, FileNotFoundError):
        pass

    # Fallback to .env
    return Settings()


settings = get_settings()
