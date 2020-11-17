# import aiohttp
# import asyncio
# from src.utils import read_links_txt
#
# links = read_links_txt('../input/images_links.txt')
#
#
# async def get(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, ssl=False) as response:
#             return response.status
#
# loop = asyncio.get_event_loop()
# tasks = [get(link) for link in links]
# results = loop.run_until_complete(asyncio.gather(*tasks))
# print("Results: %s" % results)

import asyncio
import os
import pathlib

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver

img_dir = '../img/async'
from src.utils import get_file_name_from_url

driver = webdriver.Firefox()
url_link = "https://pixabay.com/"


async def find_links(url_link):
    driver.get(url_link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = (elem.get('content') for elem in soup.find_all('meta'))
    for i in links:
        if i is not None:
            clear_links = (i for i in links if i.startswith('https') and i.endswith('.jpg') or i.endswith('.png'))
            for val in clear_links:
                yield val
                await asyncio.sleep(0.1)


pathlib.Path(img_dir).mkdir(parents=True, exist_ok=True)


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            f = await aiofiles.open(os.path.join(img_dir, get_file_name_from_url(url)), mode='wb')
            await f.write(await response.read())
            await f.close()


async def main():
    async for url in find_links(url_link):
        await download(url)


loop = asyncio.get_event_loop()
tasks = find_links(url_link)
loop.run_until_complete(main())
