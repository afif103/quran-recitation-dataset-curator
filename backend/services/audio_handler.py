import os
import shutil
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


async def organize_audio(audio_dir: str) -> str:
    organized_dir = os.path.join(settings.data_dir, "processed", "audio")
    os.makedirs(organized_dir, exist_ok=True)

    # Placeholder: assume audio files are in audio_dir, organize by reciter/surah/ayah.wav
    # For now, copy all .wav files to organized_dir
    for root, dirs, files in os.walk(audio_dir):
        for file in files:
            if file.endswith(".wav"):
                src = os.path.join(root, file)
                dst = os.path.join(organized_dir, file)
                shutil.copy2(src, dst)

    return organized_dir
