from yagdrive import GDrive

import settings

drive = GDrive()
drive.cd(settings.GDRIVE_UPLOAD_FOLDER_ID)


def upload(filepath):
    drive.put(filepath, overwrite=True)
