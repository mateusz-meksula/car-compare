"""
┌───────────────────────────────────────────────────────────────────────────────┐
│    _|_|_|                                                                     │
│  _|          _|_|_|  _|  _|_|                                                 │
│  _|        _|    _|  _|_|                                                     │
│  _|        _|    _|  _|                                                       │
│    _|_|_|    _|_|_|  _|                                                       │
│    _|_|_|                                                                     │
│  _|          _|_|    _|_|_|  _|_|    _|_|_|      _|_|_|  _|  _|_|    _|_|     │
│  _|        _|    _|  _|    _|    _|  _|    _|  _|    _|  _|_|      _|_|_|_|   │
│  _|        _|    _|  _|    _|    _|  _|    _|  _|    _|  _|        _|         │
│    _|_|_|    _|_|    _|    _|    _|  _|_|_|      _|_|_|  _|          _|_|_|   │
│                                      _|                                       │
│                                      _|                                       │
└───────────────────────────────────────────────────────────────────────────────┘

Created by Mati
"""  # noqa: E501


import asyncio
import re

from enum import Enum

from rich.console import Console

from app import factory, soups
from app.aio import get_pages_content
from app.report import Report


class SupportedSites(Enum):
    OTOMOTO = "otomoto"

    def __str__(self) -> str:
        return self.value


URL_PATTERN = re.compile(r"https://(?:www\.)?(\w+)\.\w+")


def show_welcome_message() -> None:
    print(__doc__)


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


def get_cars_data(urls: list[str], pages: list[str]) -> list[soups.CarData]:
    cars_data = []
    for url, page_content in zip(urls, pages):
        soup = factory.SoupFactory(url, page_content).get_soup()
        cars_data.append(soup.get_car_data())
    return cars_data


def print_report(cars_data: list[soups.CarData]):
    console = Console(record=True)
    report = Report(cars_data)  # type: ignore
    console.print(report)

    to_file = input("Write report to file? Y/N: ")
    if to_file.upper() == "Y":
        console.save_html("report.html")


async def main():
    show_welcome_message()
    urls = get_urls()
    pages = await get_pages_content(urls)
    cars_data = get_cars_data(urls, pages)
    print_report(cars_data)


if __name__ == "__main__":
    asyncio.run(main())
