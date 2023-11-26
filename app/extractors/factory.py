import re

from app.app_config import SupportedSites

from .extractors import OtoMotoOfferExtractor, ServiceOfferExtractor


FACTORIES: dict[SupportedSites, type[ServiceOfferExtractor]] = {}


def register_soup(
    site: SupportedSites,
    service_soup: type[ServiceOfferExtractor],
):
    FACTORIES[site] = service_soup


def extract_service_name(url: str) -> SupportedSites:
    pattern = r"https://(?:www\.)?(\w+)\.\w+"
    match = re.match(pattern, url)
    site_str = match.group(1)  # type: ignore
    return SupportedSites(site_str)


class OfferExtractorFactory:
    def __init__(self, url: str, page_content: str) -> None:
        self.url = url
        self.page_content = page_content
        self.service_name = extract_service_name(url)

    def make_extractor(self) -> ServiceOfferExtractor:
        return FACTORIES[self.service_name](
            url=self.url,
            markup=self.page_content,
        )


register_soup(SupportedSites.OTOMOTO, OtoMotoOfferExtractor)
