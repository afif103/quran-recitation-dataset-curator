from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    huggingface_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None
    kaggle_api_key: Optional[str] = None
    log_level: str = "INFO"
    data_dir: str = "data"
    backup_dir: str = "data/backup"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    s3_bucket_name: Optional[str] = None
    cerebras_model: str = "llama-3.1-8b-instant"

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()
