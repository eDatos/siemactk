import scraping
import settings
import storage
import wrangling

for dataset_url in scraping.get_datasets_urls(settings.TARGET_URL):
    print(f'Downloading {dataset_url}...')
    dataset = scraping.download_dataset(dataset_url)
    print(f'Staging {dataset}...')
    output_files = wrangling.stage_dataset(dataset)
    print('Uploading output files...')
    for file in output_files:
        storage.upload(file)
