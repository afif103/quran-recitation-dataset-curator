# Qur'an Recitation Dataset Curator

A modular Python application for collecting, cleaning, normalizing, and formatting Qur'an recitation datasets into a unified JSONL training format.

## Features

- Collect datasets from HuggingFace, Kaggle, and other sources
- Normalize transcripts to Uthmani script
- Organize audio files by reciter/surah/ayah
- Extract metadata and convert to JSONL
- Web UI via Streamlit and API via FastAPI

## Setup

1. Install dependencies: `uv pip install -r requirements.txt`
2. Set up environment: Copy `config/.env` and fill API keys
3. Run backend: `python backend/main.py`
4. Run frontend: `streamlit run frontend/app.py`

## Usage

See workflow.md for step-by-step guide.

## Architecture

- `backend/`: FastAPI app with routes and services
- `frontend/`: Streamlit UI
- `config/`: Settings and environment
- `data/`: Raw and processed data
- `tools/`: Utilities
- `docs/`: Documentation

## Requirements

- Python 3.12+
- See requirements.txt

## License

[Add license]