# Qur'an Recitation Dataset Curator

A comprehensive tool for collecting, cleaning, normalizing, and preparing Qur'an recitation datasets for AI model training. Built with Python, Streamlit, and FastAPI.

## Features

- **Dataset Collection**: Download datasets from Kaggle, HuggingFace, or custom URLs.
- **Text Normalization**: Clean and normalize Arabic text to Uthmani script, remove diacritics issues.
- **Audio Processing**: Organize audio files and generate synthetic audio using TTS for text-only datasets.
- **Metadata Extraction**: Create structured metadata for AI training.
- **JSONL Export**: Convert data to JSON Lines format for machine learning.
- **User-Friendly UI**: Streamlit interface with tabs for processing, viewing, and exporting data.
- **LLM Integration**: Optional Groq or Ollama for advanced text validation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quran-recitation-dataset-curator.git
   cd quran-recitation-dataset-curator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `config/.env`:
   ```
   GROQ_API_KEY=your_groq_api_key
   KAGGLE_API_KEY=your_kaggle_api_key
   # Optional: LANGSMITH_API_KEY, AWS keys
   ```

## Usage

### Local Development

1. Run the Streamlit app:
   ```bash
   streamlit run frontend/app.py
   ```

2. Open http://localhost:8501 in your browser.

3. Use the interface:
   - Select or enter dataset URLs.
   - Process: Download → Normalize → Organize → Extract Metadata → Convert to JSONL.
   - View results in tabs: Raw Data, Transcripts, Audio, JSONL.
   - Export processed data as ZIP.

### API Usage

The backend provides REST APIs via FastAPI (normally embedded in Streamlit, but can be run separately).

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app
│   ├── models.py            # Pydantic models
│   ├── routes/              # API endpoints
│   └── services/            # Core logic (extractor, normalizer, TTS, etc.)
├── frontend/
│   └── app.py               # Streamlit UI
├── config/
│   ├── settings.py          # Configuration
│   └── .env                 # Environment variables
├── data/
│   ├── raw/                 # Downloaded datasets
│   └── processed/           # Cleaned data, transcripts, audio, metadata
├── docs/                    # Documentation
├── tests/                   # Unit tests
├── requirements.txt         # Dependencies
└── README.md                # This file
```

## Key Components

- **Extractor**: Downloads datasets from Kaggle/HuggingFace.
- **Normalizer**: Cleans Arabic text, integrates with LLM for validation.
- **TTS**: Generates audio from text using gTTS.
- **Converter**: Creates metadata and JSONL for AI training.
- **UI**: Streamlit app for easy interaction.

## Deployment

Deploy on Streamlit Cloud:
1. Push to GitHub.
2. Go to share.streamlit.io.
3. Connect repo, set `frontend/app.py` as main file.

For production, consider Docker or cloud hosting.

## Requirements

- Python 3.12+
- API keys for Kaggle and Groq (optional for basic features)
- Internet for downloads and TTS

## Contributing

1. Fork the repo.
2. Create a feature branch.
3. Submit a pull request.

## License

[Add your license here]

## Acknowledgments

- Built for Upwork job: Qur'an Recitation AI Model Data Preparation.
- Uses libraries: Streamlit, FastAPI, gTTS, Groq, Kaggle API.