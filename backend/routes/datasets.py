from fastapi import APIRouter, HTTPException
from backend.models import DatasetDownloadRequest, DatasetDownloadResponse
from backend.services.extractor import download_datasets
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/download", response_model=DatasetDownloadResponse)
async def download(request: DatasetDownloadRequest):
    try:
        files = await download_datasets(request.sources)
        return DatasetDownloadResponse(status="success", files=files)
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
