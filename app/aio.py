import asyncio
import aiohttp

from . import errors


class StatusNot200(Exception):
    def __init__(self, url, status_code) -> None:
        super().__init__()
        self.url = url
        self.status_code = status_code


async def fetch(url: str):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as response:
            if (status_code := response.status) != 200:
                raise StatusNot200(url, status_code)
            return await response.text()


async def get_pages_content(urls: list[str]):
    try:
        pages_contents = await asyncio.gather(*[fetch(url) for url in urls])
    except StatusNot200 as exc:
        errors.FetchFailed(exc.url, exc.status_code)
    return pages_contents
