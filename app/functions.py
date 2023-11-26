import asyncio
import re
from typing import TYPE_CHECKING

import aiohttp
from rich.console import Console

from app.app_config import APP_WELCOME_MESSAGE, SupportedSites
from app.extractors.factory import OfferExtractorFactory
from app.report import Report

if TYPE_CHECKING:
    from app.extractors.extractors import CarData


URL_PATTERN = re.compile(r"https://(?:www\.)?(\w+)\.\w+")


class StatusNot200(Exception):
    def __init__(self, url, status_code) -> None:
        super().__init__()
        self.url = url
        self.status_code = status_code


async def get_page_content(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if (status_code := response.status) != 200:
                raise StatusNot200(url, status_code)
            return await response.text()


async def get_pages_contents(urls: list[str]):
    tasks = [get_page_content(url) for url in urls]
    try:
        pages_contents = await asyncio.gather(*tasks)
    except StatusNot200 as exc:
        raise SystemExit(
            f"""
    Request to {exc.url} failed.
    Status code: {exc.status_code}
            """
        )
    return pages_contents


def show_welcome_message() -> None:
    print(APP_WELCOME_MESSAGE)


def validate_url(url: str) -> tuple[bool, str | None]:
    match = re.match(URL_PATTERN, url)

    if not match:
        return False, "Invalid URL"

    site_name = match.group(1)
    try:
        SupportedSites(site_name)
    except ValueError:
        return False, f"{site_name!r} is not supported"

    return True, None


def get_urls() -> list[str]:
    print("Please enter offers' URLs:")
    print("(to stop, enter 'done')\n")

    num = 1
    urls = []
    while True:
        url = input(f"{num}: ")
        if url == "done":
            if len(urls) < 2:
                print("You have to provide at least 2 URLs")
                continue
            else:
                break

        is_valid_url, msg = validate_url(url)
        if not is_valid_url:
            print(msg)
            continue

        urls.append(url)
        num += 1

    return urls


def get_cars_data(urls: list[str], pages: list[str]) -> list["CarData"]:
    cars_data = []
    for url, page_content in zip(urls, pages):
        offer_extractor = OfferExtractorFactory(
            url=url,
            page_content=page_content,
        ).make_extractor()
        cars_data.append(offer_extractor.get_car_data())
    return cars_data


def make_report(cars_data: list["CarData"]) -> Report:
    return Report(cars_data)  # type: ignore


def show_report(report: Report):
    console = Console()
    console.print(report)
