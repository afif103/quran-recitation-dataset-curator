import pytest
from unittest.mock import patch, MagicMock
from backend.services.extractor import download_datasets


@pytest.mark.asyncio
async def test_download_general_url_success():
    sources = ["https://example.com/data.zip"]
    mock_response = MagicMock()
    mock_response.content = b"fake data"
    mock_response.raise_for_status.return_value = None
    with patch("backend.services.extractor.requests.get", return_value=mock_response):
        files = await download_datasets(sources)
        assert len(files) == 1
        assert "data.zip" in files[0]


@pytest.mark.asyncio
async def test_download_general_url_failure():
    sources = ["https://example.com/data.zip"]
    with patch(
        "backend.services.extractor.requests.get",
        side_effect=Exception("Download failed"),
    ):
        files = await download_datasets(sources)
        assert len(files) == 0


@pytest.mark.asyncio
async def test_download_kaggle_placeholder():
    sources = ["https://kaggle.com/datasets/example/quran"]
    files = await download_datasets(sources)
    assert len(files) == 0  # Placeholder, no actual download
