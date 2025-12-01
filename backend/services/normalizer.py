import os
import re
import requests
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


async def is_ollama_available() -> bool:
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


async def validate_with_llm(text: str) -> str:
    if not await is_ollama_available():
        logger.info("Ollama not available, skipping LLM validation")
        return text
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": f"You are an expert in Arabic text normalization. Ensure the text is in proper Arabic script. Normalize this Arabic text: {text}",
                "stream": False,
            },
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        logger.warning(f"LLM validation failed: {e}")
        return text  # Fallback to original


async def normalize_transcripts(transcript_files: list[str]) -> list[str]:
    normalized_files = []
    processed_dir = os.path.join(settings.data_dir, "processed", "transcripts")
    os.makedirs(processed_dir, exist_ok=True)

    for file_path in transcript_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Normalize to Uthmani: basic cleaning
            normalized_text = text
            # normalized_text = reshape(text)
            # normalized_text = get_display(normalized_text)

            # Remove non-Uthmani (placeholder, e.g., Warsh)
            # Assume Uthmani is standard, remove variants if detected
            # For now, basic cleaning: keep Arabic letters, diacritics, spaces
            normalized_text = re.sub(
                r"[^\u0600-\u06FF\u064B-\u065F\s]", "", normalized_text
            )  # Remove non-Arabic

            # LLM validation for advanced correction (log suggestion, keep basic)
            llm_suggestion = await validate_with_llm(normalized_text)
            logger.info(f"LLM suggestion for {file_path}: {llm_suggestion}")
            # Note: LLM may refuse religious text; using basic normalization

            output_path = os.path.join(processed_dir, os.path.basename(file_path))
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(normalized_text)

            normalized_files.append(output_path)
        except Exception as e:
            logger.error(f"Failed to normalize {file_path}: {e}")

    return normalized_files
