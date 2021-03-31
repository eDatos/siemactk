from pathlib import Path

from google.cloud import storage
from yagdrive import GDrive

import settings

# Google Drive
drive = GDrive()
drive.cd(settings.GDRIVE_UPLOAD_FOLDER_ID)

# Google Cloud Storage
gcs = storage.Client()
bucket = gcs.get_bucket('siemac')


def download_codelist(filepath: str):
    drive.get_by_id(settings.GDRIVE_CODELIST_ID, filepath)


def upload(file: Path):
    blob = bucket.blob(file.name)
    blob.upload_from_filename(file)
    return blob.public_url
