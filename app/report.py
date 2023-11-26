from rich import box
from rich.table import Table


class Report(Table):
    def __init__(self, cars_data: list[dict[str, str]]) -> None:
        super().__init__(
            title="Report",
            box=box.MINIMAL_HEAVY_HEAD,
        )
        self.add_column("Offer")
        for key in cars_data[0]:
            self.add_column(key.title())

        for i, car in enumerate(cars_data, start=1):
            self.add_row(str(i), *car.values())
