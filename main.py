import scraping
import settings
import storage
import wrangling
import notification
from collections import defaultdict

print('Downloading codelist...')
storage.download_codelist(settings.CODELIST_FILENAME)

uploaded_files = defaultdict(list)

for dataset_url in scraping.get_datasets_urls(settings.TARGET_URL):
    print(f'Downloading {dataset_url}...')
    dataset = scraping.download_dataset(dataset_url)

    print(f'Staging {dataset}...')
    output_files = wrangling.stage_dataset(dataset)

    print('Uploading output files...')
    for file in output_files:
        gdrive_file = storage.upload(file)
        download_url = gdrive_file['webContentLink']
        filename = file.name
        uploaded_files[dataset.stem].append((filename, download_url))
        print(f"{filename} -> {download_url}")
    print()

print('Notifying results...')
notification.notify(uploaded_files)
