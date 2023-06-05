
import os
from typing import Any, Iterable, Callable
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from time import perf_counter



async def my_get(url: str, outfile: str, sem: asyncio.Semaphore, opened_session: aiohttp.ClientSession, success_callback: Callable[[str,str], Any], fail_callback: Callable[[aiohttp.ClientResponse], Any]):
    async with sem:
        async with opened_session.get(url) as response:
            if response.status == 200:
                success_callback(outfile, await response.text())
            else:
                fail_callback(response)


async def main(urls_and_outfiles: list[tuple[str,str]], thread_count):
    semaphore = asyncio.Semaphore(thread_count)

    def on_get(outfile: str, raw_html: str):

        print('saving:', pokepaste_id)

        soup = BeautifulSoup(raw_html, 'html.parser')

        with open(outfile, 'w', encoding='utf-8') as f:
            output = '\n'.join(line for line in soup.text.splitlines() if line.strip())
            f.write(output)


    def on_fail(response: aiohttp.ClientResponse):
        print('fail', response.status)


    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *(my_get(url, outfile, semaphore, session, on_get, on_fail) for url,outfile in urls_and_outfiles)
        )
    

def download_teams(urls_and_outfiles: list[tuple[str, str]], thread_count=120):
    return asyncio.run(main(urls_and_outfiles, thread_count))


if __name__ == "__main__":
    print()

    this_dir = os.path.dirname(__file__)

    out_dir = f'{this_dir}{os.sep}team_pages'

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)


    with open('team_urls.txt') as f:
        all_urls = f.read().strip().splitlines()
        
    
    new_urls_and_outfiles = []
    for url in all_urls:
        pokepaste_id = url.rstrip('/').split('/')[-1]
        outfile = f'{out_dir}{os.sep}{pokepaste_id}.txt'

        if not os.path.exists(outfile):
            new_urls_and_outfiles.append(
                (url, outfile)
            )



    task_count = len(new_urls_and_outfiles)
    if task_count == 0:
        print(f'no urls to download; {out_dir} up to date')
        exit(0)
    
    print(f'begin dl of {task_count} urls\n')
    start = perf_counter()
    htmls = download_teams(new_urls_and_outfiles)
    finish = perf_counter()
    print('\nelapsed:', finish - start)

    print(f'\nsaved to {out_dir}')
