from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_download_datasets_endpoint():
    response = client.post(
        "/datasets/download", json={"sources": ["https://example.com/data.zip"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "files" in data


def test_normalize_transcripts_endpoint():
    response = client.post(
        "/processing/normalize", json={"transcripts": ["data/raw/transcript1.txt"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "normalized" in data


def test_organize_audio_endpoint():
    response = client.post("/processing/organize-audio", json={"audio_dir": "data/raw"})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "organized_dir" in data


def test_extract_metadata_endpoint():
    response = client.post(
        "/processing/extract-metadata",
        json={"files": ["data/processed/audio/file.wav"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "metadata" in data


def test_convert_jsonl_endpoint():
    response = client.post(
        "/processing/convert-jsonl",
        json={
            "metadata": "data/processed/metadata.json",
            "audio_dir": "data/processed/audio",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "jsonl" in data
