import os
import requests
import subprocess
import glob
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


async def download_datasets(sources: list[str]) -> list[str]:
    downloaded_files = []
    raw_dir = os.path.join(settings.data_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    for source in sources:
        try:
            if "kaggle.com" in source:
                # Handle Kaggle dataset
                parts = source.split("/")
                if len(parts) >= 6 and parts[3] == "datasets":
                    dataset = f"{parts[4]}/{parts[5]}"
                    logger.info(f"Downloading Kaggle dataset: {dataset}")
                    env = os.environ.copy()
                    if settings.kaggle_api_key:
                        env["KAGGLE_API_TOKEN"] = settings.kaggle_api_key
                    # Try different kaggle paths for cross-platform
                    kaggle_cmds = [
                        "kaggle",
                        "/home/adminuser/venv/bin/kaggle",
                        "/usr/local/bin/kaggle",
                    ]
                    result = None
                    for cmd in kaggle_cmds:
                        try:
                            result = subprocess.run(
                                [
                                    cmd,
                                    "datasets",
                                    "download",
                                    dataset,
                                    "-p",
                                    raw_dir,
                                    "--unzip",
                                ],
                                capture_output=True,
                                text=True,
                                env=env,
                                timeout=60,  # Add timeout
                            )
                            if result.returncode == 0:
                                break
                        except FileNotFoundError:
                            continue
                        except subprocess.TimeoutExpired:
                            continue
                    if result and result.returncode != 0:
                        logger.error(
                            f"Failed to download Kaggle dataset: {result.stderr}"
                        )
                    if result.returncode == 0:
                        # Find downloaded files
                        files = glob.glob(os.path.join(raw_dir, "*"))
                        downloaded_files.extend(files)
                        logger.info(f"Downloaded Kaggle dataset files: {files}")
                    else:
                        logger.error(
                            f"Failed to download Kaggle dataset: {result.stderr}"
                        )
                else:
                    logger.error(f"Invalid Kaggle URL format: {source}")
            else:
                # General download
                response = requests.get(source, timeout=30)
                response.raise_for_status()
                filename = source.split("/")[-1] or "downloaded_file"
                filepath = os.path.join(raw_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                downloaded_files.append(filepath)
                logger.info(f"Downloaded {source} to {filepath}")
        except Exception as e:
            logger.error(f"Failed to download {source}: {e}")

    return downloaded_files
