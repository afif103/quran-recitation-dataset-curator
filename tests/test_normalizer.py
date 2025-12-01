import pytest
from unittest.mock import patch, mock_open
from backend.services.normalizer import normalize_transcripts


@pytest.mark.asyncio
async def test_normalize_transcripts_success():
    transcript_files = ["data/raw/transcript1.txt"]
    mock_text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    with patch("builtins.open", mock_open(read_data=mock_text)):
        with patch(
            "backend.services.normalizer.os.path.join",
            return_value="data/processed/transcripts/transcript1.txt",
        ):
            with patch("backend.services.normalizer.os.makedirs"):
                files = await normalize_transcripts(transcript_files)
                assert len(files) == 1
                assert "transcript1.txt" in files[0]


@pytest.mark.asyncio
async def test_normalize_transcripts_failure():
    transcript_files = ["data/raw/transcript1.txt"]
    with patch("builtins.open", side_effect=Exception("File not found")):
        files = await normalize_transcripts(transcript_files)
        assert len(files) == 0
