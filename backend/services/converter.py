import os
import json
import wave
from backend.models import MetadataEntry, JsonlEntry
from config.settings import settings
from backend.services.tts import generate_audio_from_text
import logging

logger = logging.getLogger(__name__)


def get_audio_duration(file_path):
    try:
        with wave.open(file_path, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            return frames / float(rate)
    except Exception as e:
        logger.warning(f"Could not get duration for {file_path}: {e}")
        return 0.0


async def extract_metadata(files: list[str]) -> str:
    metadata = []
    processed_transcripts_dir = os.path.join(
        settings.data_dir, "processed", "transcripts"
    )

    # First, try to extract from audio files
    for file_path in files:
        # Placeholder: extract from filename or audio
        # Assume filename like reciter_surah_ayah.wav
        basename = os.path.basename(file_path)
        parts = basename.split("_")
        if len(parts) >= 3:
            try:
                reciter = parts[0]
                surah = int(parts[1])
                ayah = int(parts[2].split(".")[0])
                duration = get_audio_duration(file_path)
                sampling_rate = 16000  # Assume
                source = "unknown"
                transcript = ""  # Would load from transcript file
                audio_path = file_path
                entry = MetadataEntry(
                    reciter=reciter,
                    surah=surah,
                    ayah=ayah,
                    duration=duration,
                    sampling_rate=sampling_rate,
                    source=source,
                    transcript=transcript,
                    audio_path=audio_path,
                )
                metadata.append(entry.dict())
            except ValueError:
                # Skip files that don't match the expected format (e.g., generated files)
                continue

    # If no metadata from audio, create from processed transcripts
    if not metadata and os.path.exists(processed_transcripts_dir):
        transcript_files = [
            f
            for f in os.listdir(processed_transcripts_dir)
            if f.endswith(".txt") or f.endswith(".csv")
        ]
        for i, t_file in enumerate(transcript_files):
            transcript_path = os.path.join(processed_transcripts_dir, t_file)
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcript = f.read()
            # Dummy metadata for text-only
            entry = MetadataEntry(
                reciter="generated",
                surah=1,  # Default
                ayah=i + 1,
                duration=0,
                sampling_rate=16000,
                source="text_dataset",
                transcript=transcript,
                audio_path=f"data/processed/audio/generated_{i + 1}.wav",
            )
            metadata.append(entry.dict())

    metadata_path = os.path.join(settings.data_dir, "processed", "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return metadata_path


async def convert_to_jsonl(metadata_path: str, audio_dir: str) -> str:
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    jsonl_path = os.path.join(settings.data_dir, "processed", "dataset.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for item in metadata:
            audio_path = item["audio_path"]
            if not os.path.exists(audio_path):
                # Generate audio from transcript
                base_name = os.path.splitext(os.path.basename(audio_path))[0]
                generated_audio = os.path.join(audio_dir, f"generated_{base_name}.mp3")
                # Generate audio for longer text
                short_text = item["transcript"][:1000]  # First 1000 chars
                result = await generate_audio_from_text(short_text, generated_audio)
                if result:
                    audio_path = generated_audio
                    item["audio_path"] = audio_path  # Update metadata
            entry = JsonlEntry(
                audio_path=audio_path,
                transcript=item["transcript"],
                metadata={
                    k: v
                    for k, v in item.items()
                    if k not in ["audio_path", "transcript"]
                },
            )
            f.write(json.dumps(entry.dict(), ensure_ascii=False) + "\n")

    return jsonl_path
