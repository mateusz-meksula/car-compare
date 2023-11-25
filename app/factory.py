import re

from cc import SupportedSites

from .soups import ServiceSoup, OtoMotoSoup

FACTORIES: dict[SupportedSites, type[ServiceSoup]] = {}


def register_soup(site: SupportedSites, service_soup: type[ServiceSoup]):
    FACTORIES[site] = service_soup


def extract_service_name(url: str) -> SupportedSites:
    pattern = r"https://(?:www\.)?(\w+)\.\w+"
    match = re.match(pattern, url)
    site_str = match.group(1)  # type: ignore
    return SupportedSites(site_str)


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


register_soup(SupportedSites.OTOMOTO, OtoMotoSoup)
