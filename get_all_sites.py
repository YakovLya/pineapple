import logging
import os

import requests
from multiprocessing import Pool
import pandas as pd
import numpy as np
from functools import cache
from urllib.parse import urlparse
import coloredlogs
from tqdm import tqdm

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def read_urls():
    data = pd.read_excel('start_data/maps.xlsx')['domain'].to_numpy()[1:]
    print(f'нашел {len(data)} уникальных сайтов')
    return list(data)


@cache
def get_html_from_url(url: str):
    r = requests.get(url, headers=HEADERS, timeout=3)

    if r.status_code != 200:
        raise Exception(f'bad response code {url}\t->\t{r.status_code}')
    return r.text


def logging_exceptions(url):
    try:
        html = get_html_from_url(url)
        return html
    except Exception as ex:
        logging.error(f'in get_html_from_url:\t\t{ex}')


def read_and_write(url):
    if not isinstance(url, str):
       logging.info(f'NOT A STRING {url}') 
    elif not os.path.exists(f'urlshtml/{urlparse(url).hostname}.html'):
        html = logging_exceptions(url)
        if html is not None:
            with open(f'urlshtml/{urlparse(url).hostname}.html', 'w', encoding='utf-8') as f:
                f.write(html)
            logging.info(f'NEW {urlparse(url).hostname}.html')
    else:
        logging.info(f'ALREADY EXISTS {urlparse(url).hostname}.html')


def main():
    unique_urls = read_urls()
    for el in tqdm(unique_urls):
        read_and_write(el)
    # with Pool(3) as p:
    #     p.map(read_and_write, unique_urls)


if __name__ == '__main__':
    logging.basicConfig(filename='logs/logs_all_sites.log', filemode='a', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    main()