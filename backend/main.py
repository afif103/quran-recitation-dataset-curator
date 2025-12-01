from fastapi import FastAPI
from backend.routes import datasets, processing
from config.settings import settings
import logging

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="Qur'an Recitation Dataset Curator", version="1.0.0")

app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
app.include_router(processing.router, prefix="/processing", tags=["processing"])


@app.get("/")
def read_root():
    return {"message": "Qur'an Recitation Dataset Curator API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
