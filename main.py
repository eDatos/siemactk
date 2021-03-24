import wrangling
import scraping
import settings

for dataset_url in scraping.get_datasets_urls(settings.TARGET_URL):
    print(f'Downloading {dataset_url}...')
    dataset = scraping.download_dataset(dataset_url)
    print(f'Staging {dataset}...')
    wrangling.stage_dataset(dataset)
