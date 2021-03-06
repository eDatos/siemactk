from pathlib import Path

import pandas as pd
import settings
from google.cloud import storage
from logzero import logger
from yagdrive import GDrive

# Google Drive
drive = GDrive()

# Google Cloud Storage
gcs = storage.Client()
bucket = gcs.get_bucket('siemac')


def download_dataref(
    file_id=settings.GDRIVE_DATAREF_ID,
    filepath=settings.DATAREF_FILENAME,
    codelists_sheet=settings.DATAREF_CODELISTS_SHEET,
    inventory_sheet=settings.DATAREF_INVENTORY_SHEET,
    inventory_dataset_urls_column_name=settings.DATAREF_INVENTORY_DATASET_URLS_COLUMN_NAME,
):
    drive.get_by_id(file_id, filepath)
    fh = Path(filepath)
    codelists = pd.read_excel(fh, sheet_name=codelists_sheet, dtype=str)
    inventory = pd.read_excel(fh, sheet_name=inventory_sheet)
    logger.debug(f'Removing {filepath} file...')
    fh.unlink()  # dataref is needed no more
    return codelists, inventory[inventory_dataset_urls_column_name]


def upload(file: Path):
    blob = bucket.blob(file.name)
    blob.upload_from_filename(file)
    return blob.public_url
