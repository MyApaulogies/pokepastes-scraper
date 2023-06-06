
import os, aiohttp, asyncio
from typing import Iterable
from bs4 import BeautifulSoup, Tag
from time import perf_counter
import itertools


async def my_get(url: str, sem: asyncio.Semaphore, opened_session: aiohttp.ClientSession):
    async with sem:
        async with opened_session.get(url) as response:
            if response.status == 200:
                res = []

                soup = BeautifulSoup(await response.text(), 'html.parser')
                for tag in soup.find_all('a'):
                    tag: Tag
                    href = tag['href']
                    if '://pokepast.es' in href:
                        res.append(href)

                return res
            else: 
                print('error: status', response.status)
                return None


async def scrape_pokepastes_links_from_urls(urls, threads=120) -> Iterable:
    semaphore = asyncio.Semaphore(threads)

    async with aiohttp.ClientSession() as session:
        nested_lists = await asyncio.gather(
            *(my_get(u, semaphore, session) for u in urls)
        )

        return [url for url in itertools.chain(*nested_lists)]


if __name__ == "__main__":
    print()

    this_dir = os.path.dirname(__file__)

    out_file = f'{this_dir}{os.sep}team_urls.txt'
    meta_file = f'{this_dir}{os.sep}team_urls_meta.txt'
    tourneys_file = f'{this_dir}{os.sep}tourneys.txt'

    try:
        with open(meta_file) as f:
            visited_tourney_urls = set(f.read().strip().splitlines())
    except FileNotFoundError as e:
        visited_tourney_urls = set()

    try:
        with open(tourneys_file) as f:
            new_tourney_urls = [u for u in filter(
                lambda url: url not in visited_tourney_urls,
                f.read().strip().splitlines()
            )]

    except FileNotFoundError as e:
        print('error: no tourneys.txt file in same directory')
        exit(1)

    print(f'found {len(new_tourney_urls)} urls in {tourneys_file}')
    if len(new_tourney_urls) == 0:
        print('exiting')
        exit(0)

    print(f'start scraping\n')
    start = perf_counter()

    pokepastes_urls = asyncio.run(scrape_pokepastes_links_from_urls(new_tourney_urls))

    elapsed = perf_counter() - start
    print('\nelapsed:', elapsed)

    print(f'saving to {out_file}')
    print(f'and meta to {meta_file}')

    with open(out_file, 'a+') as o, open(meta_file, 'a+') as m:
        for url in pokepastes_urls:
            o.write(url)
            o.write('\n')
        for url in new_tourney_urls:
            m.write(url)
            m.write('\n')


