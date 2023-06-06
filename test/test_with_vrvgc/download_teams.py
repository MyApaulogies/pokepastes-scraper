
import os
from typing import Any, Iterable, Callable
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from time import perf_counter


async def my_get(url: str, sem: asyncio.Semaphore, opened_session: aiohttp.ClientSession):
    async with sem:
        async with opened_session.get(url) as response:
            if response.status == 200:
                return url, await response.text()
            else:
                return url, f'error: {response.status} ({response.url})'


async def get_async(urls, thread_count=120) -> list[str, str]:
    semaphore = asyncio.Semaphore(thread_count)

    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(my_get(u, semaphore, session) for u in urls)
        )


def pokepaste_id(url): 
    return url.rstrip('/').split('/')[-1]


if __name__ == "__main__":
    print()

    this_dir = os.path.dirname(__file__)
    out_dir = f'{this_dir}{os.sep}team_pages'
    team_urls_file = f'{this_dir}{os.sep}team_urls.txt'

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)


    with open(team_urls_file) as f:
        all_urls = f.read().strip().splitlines()
        
    new_urls = []
    for url in all_urls:
        outfile = f'{out_dir}{os.sep}{pokepaste_id(url)}.html'

        if not os.path.exists(outfile):
            new_urls.append(url)
        
    
    task_count = len(new_urls)
    if task_count == 0:
        print(f'no urls to download - \n{out_dir}\nis up to date according to\n{team_urls_file}')
        exit(0)
    
    print(f'{task_count} new urls found in {out_dir}')
    print(f'begin dl\n')
    start = perf_counter()

    results = asyncio.run(get_async(new_urls))

    elapsed = perf_counter() - start
    print('\nelapsed:', elapsed)


    for url, raw_html in results:
        outfile = f'{out_dir}{os.sep}{pokepaste_id(url)}.html'
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(raw_html)
        

    print(f'\nall saved to {out_dir}')
