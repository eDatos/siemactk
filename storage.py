from yagdrive import GDrive

import settings

drive = GDrive()
drive.cd(settings.GDRIVE_UPLOAD_FOLDER_ID)


def upload(filepath):
    return drive.put(filepath, overwrite=True)


def download_codelist(filepath):
    drive.get_by_id(settings.GDRIVE_CODELIST_ID, output_filename=settings.CODELIST_FILENAME)
