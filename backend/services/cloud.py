import os
import boto3
from botocore.exceptions import NoCredentialsError
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


def upload_to_s3(file_path: str, bucket: str, s3_key: str) -> str:
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        logger.warning("AWS credentials not set, skipping S3 upload")
        return ""

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

    try:
        s3.upload_file(file_path, bucket, s3_key)
        url = f"https://{bucket}.s3.amazonaws.com/{s3_key}"
        logger.info(f"Uploaded {file_path} to {url}")
        return url
    except NoCredentialsError:
        logger.error("AWS credentials invalid")
        return ""
    except Exception as e:
        logger.error(f"S3 upload failed: {e}")
        return ""
