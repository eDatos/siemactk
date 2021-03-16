import re
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DATASET_URL = (
    'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/'
    'BulkDownloadListing?file=data/{dataset_code}.tsv.gz'
)


def get_datasets_urls(target_url):
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get(target_url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#gepRegionIndicators .tipTable'))
    )

    items = element.find_elements_by_class_name('tipRow')

    datasets_urls = []
    for item in items:
        item_id = item.get_attribute('id')
        dataset_code = re.match(r'tipRow_[\d-]+_(.*)', item_id).group(1)
        dataset_table_url = BASE_DATASET_URL.format(dataset_code=dataset_code)
        datasets_urls.append(dataset_table_url)

    return datasets_urls


if __name__ == '__main__':
    target_url = sys.argv[1]
    print(get_datasets_urls(target_url))
