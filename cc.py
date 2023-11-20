r"""[bold][blue]
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
[/bold]

for help, type [yellow]python cc.py --help[/yellow]
"""  # noqa: E501


import argparse
import asyncio
import re
import time

from rich import print
from rich.console import Console
from rich_argparse import RichHelpFormatter

from app import errors, factory, soups
from app.aio import get_pages_content
from app.report import Report


SUPPORTED_SITES = ["otomoto"]

URL_PATTERN = re.compile(r"https://(?:www\.)?(\w+)\.\w+")


console = Console()

factory.register_soup("otomoto", soups.OtoMotoSoup)


def validate_offers_number(value):
    try:
        value = int(value)
    except ValueError:
        errors.OffersNotAnInteger(value)

    if value < 2:
        errors.OffersLessThat2(value)

    return value


class CarCompare(argparse.ArgumentParser):
    offers: int
    with_file: bool
    urls: list[str]

    def __init__(self) -> None:
        super().__init__(
            usage="cc.py offers [-h] [-f]",
            formatter_class=RichHelpFormatter,
        )

        self.add_argument(
            "offers",
            nargs="?",
            type=validate_offers_number,
            help="Number of car offers. Must be an integer greater than 1.",  # noqa: E501
        )
        self.add_argument(
            "-f",
            "--file",
            help="If present, application will save report to an HTML file.",  # noqa: E501
            action="store_true",
        )

        args = self.parse_args()

        self.offers = args.offers
        if self.offers is None:
            print(__doc__)
            quit()

        self.with_file = args.file
        self.urls = []
        self.get_offers_urls()

    def get_offers_urls(self) -> None:
        num = 1
        print("\n[blue]Please enter offers' URLs:")
        while len(self.urls) < self.offers:
            user_url = console.input(f"[blue]{num} -> : ")
            if not self._validate_url(user_url):
                errors.invalid_url()
                continue
            else:
                self.urls.append(user_url)
                num += 1

    def _validate_url(self, url: str) -> bool:
        if url in self.urls:
            return False

        match = re.match(URL_PATTERN, url)

        if not match:
            return False

        site_name = match.group(1)
        if site_name not in SUPPORTED_SITES:
            return False

        return True

    async def __call__(self) -> None:
        pages_content = await get_pages_content(self.urls)
        cars_data = [
            factory.SoupFactory(
                url=url,
                page_content=page_content,
            )().get_car_data()
            for url, page_content in zip(self.urls, pages_content)
        ]

        record = self.with_file
        console = Console(record=record)
        report = Report(cars_data)  # type: ignore
        print()
        console.print(report)
        if self.with_file:
            console.save_html("report.html")


def exit_app():
    print("\n")
    print("Exiting", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", flush=True, end="")
    quit()


if __name__ == "__main__":
    try:
        app = CarCompare()
        asyncio.run(app())
    except KeyboardInterrupt:
        exit_app()
