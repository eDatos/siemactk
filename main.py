import sys

import scraper

target_url = sys.argv[1]
for dataset_url in scraper.get_datasets_urls(target_url):
    print(f'Downlading {dataset_url}...')
    dataset = scraper.download_dataset(dataset_url)
    print(f'Filtering {dataset}...')
    scraper.filter_dataset(dataset)
