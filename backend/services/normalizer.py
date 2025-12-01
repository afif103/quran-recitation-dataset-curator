import os
import re
import requests
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


async def validate_with_llm(text: str) -> str:
    if not settings.groq_api_key:
        logger.info("Groq API key not set, skipping LLM validation")
        return text
    # Chunk the text to avoid token limits
    chunk_size = 500
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    normalized_chunks = []
    for chunk in chunks:
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"You are an expert in Arabic text normalization. Ensure the text is in proper Arabic script. Normalize this Arabic text: {chunk}",
                        },
                    ],
                    "max_tokens": 300,
                    "temperature": 0.1,
                },
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            normalized = result["choices"][0]["message"]["content"].strip()
            normalized_chunks.append(normalized)
        except requests.exceptions.HTTPError as e:
            logger.warning(
                f"LLM validation failed for chunk (HTTP): {e.response.status_code} - {e.response.text}"
            )
            normalized_chunks.append(chunk)  # Fallback to original chunk
        except Exception as e:
            logger.warning(f"LLM validation failed for chunk: {e}")
            normalized_chunks.append(chunk)  # Fallback to original chunk
    return "".join(normalized_chunks)


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
