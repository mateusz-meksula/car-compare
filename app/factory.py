import re

from .soups import ServiceSoup

FACTORIES: dict[str, type[ServiceSoup]] = {}


def register_soup(site: str, service_soup: type[ServiceSoup]):
    FACTORIES[site] = service_soup


def extract_service_name(url: str) -> str:
    pattern = r"https://(?:www\.)?(\w+)\.\w+"
    match = re.match(pattern, url)
    return match.group(1)  # type: ignore


class SoupFactory:
    def __init__(self, url: str, page_content: str) -> None:
        self.url = url
        self.page_content = page_content
        self.service_name = extract_service_name(url)

    def get_soup(self) -> ServiceSoup:
        return FACTORIES[self.service_name](
            url=self.url,
            markup=self.page_content,
        )
