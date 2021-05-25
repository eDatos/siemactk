import gzip
import re
from pathlib import Path

import requests
from logzero import logger

import settings


def download_dataset(dataset_url, target_folder=settings.DATASETS_DIR):
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(dataset_url)
        filename = re.search(
            r'filename="(.*).tsv.gz"', r.headers['Content-Disposition']
        ).group(1)
    except Exception as err:
        err_type = err.__class__.__name__
        logger.error(f'{err_type}: {err}')
        return None
    f = target_folder / (filename + '.tsv')
    f.write_bytes(gzip.decompress(r.content))
    return f
