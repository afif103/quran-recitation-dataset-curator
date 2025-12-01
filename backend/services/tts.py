import asyncio
from gtts import gTTS
import logging

logger = logging.getLogger(__name__)


async def generate_audio_from_text(text: str, output_path: str, lang: str = "ar"):
    try:
        loop = asyncio.get_event_loop()
        tts = await loop.run_in_executor(
            None, lambda: gTTS(text=text, lang=lang, slow=False)
        )
        await loop.run_in_executor(None, tts.save, output_path)
        logger.info(f"Generated audio: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to generate audio: {e}")
        return None
