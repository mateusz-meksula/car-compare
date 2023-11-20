import re
from dataclasses import dataclass

from .soups import ServiceSoup

FACTORIES: dict[str, type[ServiceSoup]] = {}


def register_soup(site: str, service_soup: type[ServiceSoup]):
    FACTORIES[site] = service_soup


def extract_service_name(url: str) -> str:
    pattern = r"https://(?:www\.)?(\w+)\.\w+"
    match = re.match(pattern, url)
    return match.group(1)  # type: ignore


@dataclass
class SoupFactory:
    url: str
    page_content: str

    def __post_init__(self):
        self.service_name = extract_service_name(self.url)

    def __call__(self) -> ServiceSoup:
        return FACTORIES[self.service_name](
            url=self.url,
            markup=self.page_content,
        )
