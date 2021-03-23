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
TARGET_GEOCODES = config(
    'TARGET_GEOCODES', default='ES70,PT20,PT30,EU27_2020', cast=config.list
)
CODELIST = config('CODELIST', default='codelist.csv')
RECODING_LANGUAGES = config('RECODING_LANGUAGES', default='ES,PT', cast=config.list)
