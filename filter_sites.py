import logging
import os
from multiprocessing import Pool
import itertools
import shutil
import coloredlogs

KEY_WORDS = ['недвиж', 'дом', 'квартир', 'площад', 'build', 'property', 'apartmen', 'строит']

def filter_property(name, text):
    for word in KEY_WORDS:
        if word in text:
            return True
    logging.info(f'not property: {name}')
    return False

def filter_empty_file(name, text):
    if len(text) < 2:
        return False
    return True


FILTERS = [filter_empty_file, filter_property]


def all_filters(name_text):
    if name_text is None:
        return False
    name, text = name_text
    global FILTERS
    res = list()
    for func in FILTERS:
        res.append(func(name, text))

    return all(res)


def read_file(name):
    try:
        with open(f'urlshtml/{name}', 'r', encoding='utf-8') as f:
            return name, f.read()
    except UnicodeDecodeError:
        logging.error(f'problem with encoding:\t{name}')


def read_and_filter(name):
    return all_filters(read_file(name))


def main():
    names = os.listdir('urlshtml')
    with Pool(5) as p:
        filter_list = p.map(read_and_filter, os.listdir('urlshtml'))
    
    good_names = list(itertools.compress(names, filter_list))
    logging.info(f'WAS {len(names)} -> BECAME {len(good_names)}')

    for name in good_names:
        shutil.copy(f'urlshtml/{name}', f'out/filtered_sites/{name}')


if __name__ == '__main__':
    logging.basicConfig(filename='logs/logs_filter_sites.log', filemode='a', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    main()
