import scraper
import settings

for dataset_url in scraper.get_datasets_urls(settings.TARGET_URL):
    print(f'Downlading {dataset_url}...')
    dataset = scraper.download_dataset(dataset_url)
    print(f'Filtering & cleaning {dataset}...')
    scraper.clean_dataset(dataset)
