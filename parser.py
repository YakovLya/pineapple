import pandas as pd
import numpy as np
import os, re
from tqdm import tqdm

data = []
for url in os.listdir('out/filtered_sites'):
    file = open('out/filtered_sites/' + url, 'r')
    try:
        html = file.read()
    except:
        continue
    for phone in re.findall('tel:\+?[\d\s()-]{10,}', html): # Телефоны
        if [url, phone[4:], 'phone'] not in data:
            data.append([url, phone[4:], 'phone'])
    for code in re.findall('ОГРН[\s:-]+\d{13}', html): # ОГРН
        if [url, code, 'ОГРН'] not in data:
            data.append([url, code, 'ОГРН'])
    for code in re.findall('ОГРНИП[\s:-]+\d{15}', html): # ОГРНИП (приравниваю к ОГРН)
        if [url, code, 'ОГРН'] not in data:
            data.append([url, code, 'ОГРН'])
    for code in re.findall('ИНН[\s:-]+\d{10}', html): # ИНН
        if [url, code, 'ИНН'] not in data:
            data.append([url, code, 'ИНН'])
    for mail in re.findall('mailto:[\w\d]+@[\w\d]+.\w{2,}', html): # Почта
        if [url, mail[7:], 'email'] not in data:
            data.append([url, mail[7:], 'email'])
data = np.unique(data, axis=0).tolist()

with open('out/out.txt', 'w') as f:
    f.write(str(data))