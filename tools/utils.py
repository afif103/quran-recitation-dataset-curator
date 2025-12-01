import os
import shutil
import logging

logger = logging.getLogger(__name__)


def backup_data(source_dir: str, backup_dir: str):
    if os.path.exists(source_dir):
        shutil.copytree(source_dir, backup_dir, dirs_exist_ok=True)
        logger.info(f"Backed up {source_dir} to {backup_dir}")


def validate_file_exists(file_path: str) -> bool:
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    return True


def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path) if os.path.exists(file_path) else 0
