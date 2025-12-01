import asyncio
from backend.services.normalizer import normalize_transcripts


async def test():
    files = await normalize_transcripts(["data/raw/transcript1.txt"])
    print("Normalized files:", files)


asyncio.run(test())
