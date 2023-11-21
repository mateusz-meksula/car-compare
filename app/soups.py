import json

from abc import ABC, abstractmethod
from typing import TypedDict

from bs4 import BeautifulSoup

from . import errors

with open("./app/soups_config.json", encoding="utf-8") as f:
    soups_config = json.load(f)


class CarData(TypedDict):
    price: str
    brand: str
    model: str
    production_year: str
    mileage: str
    capacity: str
    fuel: str
    power: str
    gearbox: str


class ServiceSoup(BeautifulSoup, ABC):
    def __init__(self, url: str, markup: str) -> None:
        super().__init__(markup, "html.parser")
        self.url = url

    @property
    @abstractmethod
    def config(self):
        ...

    @abstractmethod
    def get_car_data(self) -> CarData:
        ...


class OtoMotoSoup(ServiceSoup):
    @property
    def config(self) -> dict[str, str]:
        return soups_config["otomoto"]

    def get_car_data(self) -> CarData:
        car_data: CarData = {}  # type: ignore
        mapping = self.config.copy()

        price_class_name = mapping.pop("price")
        price_tag = self.find("h3", class_=price_class_name)
        if price_tag is None:
            errors.InvalidPageContent(self.url)
        car_data["price"] = price_tag.get_text() + " PLN"

        for k, v in mapping.items():
            tag = self.find("p", string=v)
            sibling_text = "-------"
            if tag is not None:
                sibling = tag.find_next(["p", "a"])
                if sibling:
                    sibling_text = sibling.get_text()
            car_data[k] = sibling_text
        return car_data
