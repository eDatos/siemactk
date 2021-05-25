import re
from collections import defaultdict

import logzero

import notification
import scraping
import settings
import storage
import wrangling


def init_logger():
    console_logformat = (
        '%(asctime)s '
        '%(color)s'
        '[%(levelname)-8s] '
        '%(end_color)s '
        '%(message)s '
        '%(color)s'
        '(%(filename)s:%(lineno)d)'
        '%(end_color)s'
    )
    # remove colors on logfile
    file_logformat = re.sub(r'%\((end_)?color\)s', '', console_logformat)

    console_formatter = logzero.LogFormatter(fmt=console_logformat)
    file_formatter = logzero.LogFormatter(fmt=file_logformat)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger


def run():

    logger = init_logger()

    logger.info('Downloading dataref file...')
    codelists, datasets_urls = storage.download_dataref()

    logger.info('Converting codelists to dict mapping...')
    codelists = wrangling.codelists_to_dict(codelists)

    uploaded_files = defaultdict(list)

    for dataset_url in datasets_urls:
        logger.info(f'Downloading {dataset_url}')
        if dataset := scraping.download_dataset(dataset_url):
            logger.info(f'Staging {dataset}...')
            if output_files := wrangling.stage_dataset(dataset, codelists):
                logger.info('Uploading output files...')
                for file in output_files:
                    download_url = storage.upload(file)
                    filename = file.name
                    uploaded_files[dataset.stem].append((filename, download_url))
                    logger.debug(f'{filename} -> {download_url}')

    logger.info('Notifying results...')
    notification.notify(uploaded_files)


if __name__ == '__main__':
    run()
