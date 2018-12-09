from bs4 import BeautifulSoup
from selenium import webdriver
import re
import os
import random

options = webdriver.ChromeOptions()
options.add_argument('--headless')

# c major
zeros_in_hist_major = [
    1, 3, 6, 8, 10
]

# d minor
zeros_in_hist_minor = [
    1, 3, 6, 8, 11
]

def replace_minus(t):
    for i in range(3):
        if t[i] == '-':
            t[i] = int(t[1])
        else:
            t[i] = int(t[i])
    return t

def build_histogram(d, zeros):
    result = []
    d_i = 0
    for i in range(12):
        if i in zeros:
            result.append(0)
        elif d_i < len(d):
            result.append(int((d[d_i][0] - d[d_i][1]) * 5 / (d[d_i][2] - d[d_i][1])) + (random.random() > 0.5))
            d_i += 1
        else:
            result.append(int((result[d_i-len(d)] + result[d_i-len(d)+1]) / 2) + (random.random() > 0.5))
    return result

def get_real_data():
    browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    browser.get('http://aqicn.org/city/usa/kansas/wy/kc/')

    html = browser.page_source
    browser.close()
    soup = BeautifulSoup(html, 'html.parser')

    data = [
        soup.find('tr', {'id': 'tr_pm25'}),
        soup.find('tr', {'id': 'tr_pm10'}),
        soup.find('tr', {'id': 'tr_no2'}),
        soup.find('tr', {'id': 'tr_so2'})
    ]
    gen_data = list(map(lambda e: [e.find('td', id=re.compile('^cur_')).decode_contents(), e.find('td', id=re.compile('^min_')).decode_contents(), e.find('td', id=re.compile('^max_')).decode_contents()], data))
    aggregate = int(soup.find('div', {'class': 'aqivalue'}).decode_contents())
    return gen_data, aggregate


def get_data():
    gen_data, aggregate = get_real_data()
    notes_per_second = max(aggregate / 200 * 16, 1)
    temperature = max(aggregate / 150 * 2, 1)

    # list of lists containing (current, min, max) for each pollution metric
    gen_data = list(map(lambda e: replace_minus(e), gen_data))
    primer_melody = list(map(lambda e: int((e[0] - e[1]) * 127 / (e[2] - e[1])), gen_data))

    zeros = zeros_in_hist_major if aggregate < 100 else zeros_in_hist_minor
    histogram = build_histogram(gen_data, zeros)
    print(primer_melody, histogram, notes_per_second, temperature)
    return primer_melody, histogram, notes_per_second, temperature