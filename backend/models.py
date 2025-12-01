from pydantic import BaseModel
from typing import List, Dict, Any


class DatasetDownloadRequest(BaseModel):
    sources: List[str]  # List of URLs from HuggingFace/Kaggle


class DatasetDownloadResponse(BaseModel):
    status: str
    files: List[str]


class NormalizeRequest(BaseModel):
    transcripts: List[str]  # List of transcript file paths


class NormalizeResponse(BaseModel):
    status: str
    normalized: List[str]


class OrganizeAudioRequest(BaseModel):
    audio_dir: str


class OrganizeAudioResponse(BaseModel):
    status: str
    organized_dir: str


class ExtractMetadataRequest(BaseModel):
    files: List[str]


class ExtractMetadataResponse(BaseModel):
    status: str
    metadata: str  # Path to metadata.json


class ConvertJsonlRequest(BaseModel):
    metadata: str
    audio_dir: str


class ConvertJsonlResponse(BaseModel):
    status: str
    jsonl: str  # Path to dataset.jsonl


class MetadataEntry(BaseModel):
    reciter: str
    surah: int
    ayah: int
    duration: float
    sampling_rate: int
    source: str
    transcript: str
    audio_path: str


class JsonlEntry(BaseModel):
    audio_path: str
    transcript: str
    metadata: Dict[str, Any]
