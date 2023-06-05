
import os
from typing import Iterable
import requests
from bs4 import BeautifulSoup, Tag


with open('tourneys.txt') as f:
    tourney_urls = f.read().splitlines()

from time import time


team_urls = []
get_elapsed = []
parse_elapsed = []


print('begin scraping\n')
scrape_start = time()

with requests.Session() as session:
    for url in tourney_urls:
        print(f'requests.get {url}:')
        get_start = time()
        res = session.get(url)
        get_end = time()
        get_elapsed.append(get_end - get_start)
        print(f'-> elapsed: {get_end - get_start}\n')

        print(f'parse + scrape {url}:')
        parse_start = time()
        soup = BeautifulSoup(res.text, 'html.parser')

        for tag in soup.find_all('a'):
            tag: Tag
            href = tag['href']
            if '://pokepast.es' in href:
                assert href.startswith('https://pokepast.es/')

                team_urls.append(href)

        parse_end = time()
        parse_elapsed.append(parse_end - parse_start)
        print(f'-> elapsed: {parse_end - parse_start}\n')


def avg(e: Iterable[int]):
    return sum(e) / len(e)


print('\nscraping complete')
print(f'- elapsed: {time() - scrape_start}')
print(f'- average get time: {avg(get_elapsed)}')
print(f'- average parse time: {avg(parse_elapsed)}')

this_dir = os.path.dirname(__file__)
outfile = f'{this_dir}{os.sep}team_urls.txt'

i = 1
while os.path.exists(outfile):
    outfile = f'{this_dir}{os.sep}team_urls({i}).txt'
    i += 1

with open(outfile, 'w') as f:
    for url in team_urls:
        f.write(f"{url}\n")

print(f'\nsaved to {outfile}')