from collections import defaultdict

import notification
import scraping
import storage
import wrangling

print('Downloading dataref file...')
codelists, datasets_urls = storage.download_dataref()

print('Converting codelists to dict mapping...')
codelists = wrangling.codelists_to_dict(codelists)

uploaded_files = defaultdict(list)

for dataset_url in datasets_urls:
    print(f'Downloading {dataset_url}...')
    dataset = scraping.download_dataset(dataset_url)

    print(f'Staging {dataset}...')
    output_files = wrangling.stage_dataset(dataset, codelists)

    print('Uploading output files...')
    for file in output_files:
        download_url = storage.upload(file)
        filename = file.name
        uploaded_files[dataset.stem].append((filename, download_url))
        print(f"{filename} -> {download_url}")
    print()

print('Notifying results...')
notification.notify(uploaded_files)
