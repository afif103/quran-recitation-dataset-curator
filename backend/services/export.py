import zipfile
import os
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


def export_data(output_zip: str) -> str:
    processed_dir = os.path.join(settings.data_dir, "processed")
    if not os.path.exists(processed_dir):
        logger.error("Processed data directory not found")
        return ""

    try:
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(processed_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, processed_dir)
                    zipf.write(file_path, arcname)
        logger.info(f"Exported data to {output_zip}")
        return output_zip
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return ""
