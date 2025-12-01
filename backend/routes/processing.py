from fastapi import APIRouter, HTTPException
from backend.models import (
    NormalizeRequest,
    NormalizeResponse,
    OrganizeAudioRequest,
    OrganizeAudioResponse,
    ExtractMetadataRequest,
    ExtractMetadataResponse,
    ConvertJsonlRequest,
    ConvertJsonlResponse,
)
from backend.services import normalizer, audio_handler, converter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/normalize", response_model=NormalizeResponse)
async def normalize_transcripts(request: NormalizeRequest):
    try:
        normalized = await normalizer.normalize_transcripts(request.transcripts)
        return NormalizeResponse(status="success", normalized=normalized)
    except Exception as e:
        logger.error(f"Normalization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/organize-audio", response_model=OrganizeAudioResponse)
async def organize_audio(request: OrganizeAudioRequest):
    try:
        organized_dir = await audio_handler.organize_audio(request.audio_dir)
        return OrganizeAudioResponse(status="success", organized_dir=organized_dir)
    except Exception as e:
        logger.error(f"Audio organization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-metadata", response_model=ExtractMetadataResponse)
async def extract_metadata(request: ExtractMetadataRequest):
    try:
        metadata_path = await converter.extract_metadata(request.files)
        return ExtractMetadataResponse(status="success", metadata=metadata_path)
    except Exception as e:
        logger.error(f"Metadata extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/convert-jsonl", response_model=ConvertJsonlResponse)
async def convert_to_jsonl(request: ConvertJsonlRequest):
    try:
        jsonl_path = await converter.convert_to_jsonl(
            request.metadata, request.audio_dir
        )
        return ConvertJsonlResponse(status="success", jsonl=jsonl_path)
    except Exception as e:
        logger.error(f"JSONL conversion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
