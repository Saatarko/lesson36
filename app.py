import asyncio

import aiohttp
from bs4 import BeautifulSoup
from aiohttp import web


async def get_current_usd_rate(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            html_content = await response.text()
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup
        elif response.status == 423:
            print("Сайт заблокирован")
            return None
        else:
            return print("К сожалению страница для парсинга недоступна")


def parse_titles(soup):
    # Ищем все div элементы, у которых класс содержит слово 'title'
    titles = soup.select('div[class*="title"]')
    return [title.get_text(strip=True) for title in titles]


async def main():
    # url = 'https://5element.by'
    url = 'https://www.onliner.by'

    async with aiohttp.ClientSession() as session:
        soup = await get_current_usd_rate(session, url)
        if soup:
            titles = parse_titles(soup)
            print(titles)
        else:
            print("На странице заголовков не найдено")

    await asyncio.sleep(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except RuntimeError as e:
        print(f"Ошибка: {e}")

