from yagdrive import GDrive

import settings

drive = GDrive()
drive.cd(settings.GDRIVE_UPLOAD_FOLDER_ID)


def upload(filepath):
    return drive.put(filepath, overwrite=True)


def download_codelist(filepath):
    f, _ = drive.get_by_id(settings.GDRIVE_CODELIST_ID, mimetype='text/csv')
    f.rename(filepath)
