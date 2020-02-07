"""
Populates an S3 bucket for the FIF Archive
"""

# Standard library
import os
import csv
import logging
from pathlib import Path

# Third party modules
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError


def upload(file_path, key, bucket):
    """Uploads a file to S3

    Args:
        file_path (str): The path to the file to upload
        bucket (Bucket): boto3 Bucket object to upload to
        key (str): The name of the key to upload to

    Returns:
        boolean: Whether the operation succeeded

    Raises:
        ClientError
    """

    try:
        bucket.upload_file(Filename=file_path, Key=key)
    except ClientError as e:
        logging.error(e)
        return False
    return True


BASEDIR = Path(__file__).parent.resolve()
env_path = BASEDIR / '.env'
load_dotenv(dotenv_path=env_path)

s3_resource = boto3.resource(
    's3',
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY')
)

bucket = s3_resource.Bucket(os.getenv('S3_FIF_BUCKET_NAME'))

with open(os.getenv('FIF_MAP'), newline='') as csvfile:
    FIF_FOLDER = Path(os.getenv('FIF_FOLDER'))
    reader = csv.DictReader(csvfile)
    for row in reader:
        fif_path = FIF_FOLDER / row['Filename']
        key = f"{row['UNI']}/{row['Filename']}"
        upload(file_path=fif_path.as_posix(), key=key, bucket=bucket)
