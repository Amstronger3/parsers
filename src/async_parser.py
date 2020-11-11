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

from src.async_parser import img_dir
from src.utils import get_file_name_from_url

driver = webdriver.Firefox()
url_link = "https://pixabay.com/"


def find_links(url_link):
    driver.get(url_link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    clear_links = list()
    links = (elem.get('content') for elem in soup.find_all('meta'))
    for i in links:
        if i is not None:
            if i.startswith('https') and i.endswith('.jpg') or i.endswith('.png'):
                clear_links.append(i)
    return clear_links


pathlib.Path(img_dir).mkdir(parents=True, exist_ok=True)


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            f = await aiofiles.open(os.path.join(img_dir, get_file_name_from_url(url)), mode='wb')
            await f.write(await response.read())
            await f.close()


line = find_links(url_link)
loop = asyncio.get_event_loop()
tasks = [download(link) for link in line]
loop.run_until_complete(asyncio.gather(*tasks))
