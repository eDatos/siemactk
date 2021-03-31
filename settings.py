from prettyconf import config

TARGET_URL = config(
    'TARGET_URL',
    default='https://ec.europa.eu/eurostat/cache/RCI/myregion/'
    '#?reg=ES70&ind=1-2_demo_r_d2jan',
)
BASE_DATASET_URL = config(
    'BASE_DATASET_URL',
    default='https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/'
    'BulkDownloadListing?file=data/',
)
DATASETS_DIR = config('DATASETS_DIR', default='data')
TARGET_GEOCODES = config(
    'TARGET_GEOCODES', default='ES70,PT20,PT30,EU27_2020', cast=config.list
)
RECODING_LANGUAGES = config('RECODING_LANGUAGES', default='ES,PT', cast=config.list)

CODELIST_FILENAME = config('CODELIST_FILENAME', default='codelist.xlsx')
GDRIVE_CODELIST_ID = config('GDRIVE_CODELIST_ID')
CODELIST_RECODE_SHEET = config('CODELIST_RECODE_SHEET')

GDRIVE_API_CREDENTIALS = config('GDRIVE_API_CREDENTIALS', default='gdrive-credentials.json')
GDRIVE_API_SECRETS = config('GDRIVE_API_SECRETS', default='gdrive-secrets.json')
GDRIVE_UPLOAD_FOLDER_ID = config('GDRIVE_UPLOAD_FOLDER_ID')

NOTIFICATION_FROM_ADDR = config('NOTIFICATION_FROM_ADDR')
NOTIFICATION_TO_ADDRS = config('NOTIFICATION_TO_ADDRS', cast=config.list)
SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT')
SMTP_USERNAME = config('SMTP_USERNAME')
SMTP_PASSWORD = config('SMTP_PASSWORD')
