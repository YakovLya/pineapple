import os

import pandas as pd
import numpy as np
import requests
from urlextract import URLExtract
import itertools
from urllib.parse import urlparse
import datetime as dt
import logging
import coloredlogs
from multiprocessing import Pool
import shutil

IGNORED_URLS = list()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
KEY_WORDS = ['недвиж', 'дом', 'квартир', 'площад', 'build', 'property', 'apartmen', 'строит']


def read_urls():
    data = np.unique(np.concatenate([pd.read_excel('clients.xlsx')['domain'].to_numpy()[1:],
                                     pd.read_excel('spark.xlsx')['domain'].to_numpy()[1:]]))
    print(f'нашел {len(data)} уникальных сайтов')
    return list(data)


def is_url_ok(url: str):
    global IGNORED_URLS
    parsed = urlparse(url)
    # check url is not numbers
    if not any(c.isalpha() for c in url):
        return False
    # check ignored
    if parsed.hostname is None:
        return False
    if parsed.hostname in IGNORED_URLS or parsed.hostname[4:] in IGNORED_URLS:
        return False
    if len(parsed.hostname.split('.')[0]) < 3:
        return False
    return True


def check_property(text):
    global KEY_WORDS
    formatted = text.lower()
    for word in KEY_WORDS:
        if word in formatted:
            return True
    return False


def correct_url(url: str):
    # contains protocol
    if not '://' in url:
        return 'http://' + url
    return url


def searching_other_urls(url_list, depth=2):
    if depth == 0:
        return [el for el in list(url_list) if is_url_ok(el)]
    else:
        html_list = list()
        for url in url_list:
            try:
                r = requests.get(url, headers=HEADERS)
                if r.status_code != 200:
                    logging.critical(f'{url}\t:\t{r.status_code}')
                    continue
                html_list.append(r.text)
            except requests.exceptions.ConnectionError:
                pass
            except Exception as ex:
                logging.error(f'{url}\t:\t{ex}')

        extractor = URLExtract()
        clear_urls = [correct_url(el) for el in
                      itertools.chain(*map(extractor.find_urls, html_list)) if is_url_ok(el)]
        return searching_other_urls(list(np.unique(clear_urls + url_list)), depth - 1)


def parsing_hostname_and_scheme(url_list):
    res = list()
    for url in url_list:
        try:
            r = requests.get(url, headers=HEADERS)
            if r.status_code == 200:
                res.append(urlparse(url).scheme + '://' + urlparse(url).hostname)
        except Exception as ex:
            logging.critical(f'bad url {url}')

    return np.unique(res)


def write_data_file(url: str):
    """dir_path is for folder, where connected urls are stored"""
    if is_url_ok(url):
        host = urlparse(url).hostname
        if not os.path.exists(f'results/{host}'):
            try:
                r = requests.get(url, headers=HEADERS)

                if r.status_code != 200:
                    logging.critical(f'{url}\t:\t{r.status_code}')
                else:
                    if check_property(r.text):
                        res = parsing_hostname_and_scheme(searching_other_urls([url]))
                        os.mkdir(f'results/{host}')
                        for el in res:
                            with open(f'results/{host}/{urlparse(el).hostname}.html', 'w',
                                      encoding='utf-8') as f:
                                html_text = requests.get(el, headers=HEADERS).text
                                if len(html_text) > 1:
                                    f.write(html_text)
                    else:
                        logging.warning(f'not property url : {url}')
            except requests.exceptions.ConnectionError:
                logging.error(f'{url}')
        else:
            logging.info(f'{host} already exists')


def main():
    coloredlogs.install()
    unique_urls = list(map(correct_url, read_urls()))
    with Pool(30) as p:
        p.map(write_data_file, unique_urls)
    # _ = [write_data_file(el) for el in unique_urls]
    # write_data_file('https://amp-project.pro/')


if __name__ == '__main__':
    with open('ignored_urls.txt', 'r') as f:
        IGNORED_URLS = list(map(lambda x: x.rstrip(), f.readlines()))

    main()
