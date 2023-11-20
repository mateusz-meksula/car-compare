from rich import box
from rich.table import Table


class Report(Table):
    def __init__(self, cars_data: list[dict[str, str]]) -> None:
        super().__init__(
            title="Report",
            box=box.MINIMAL_HEAVY_HEAD,
            title_style="bold blue",
            header_style="bold yellow",
        )
        self.add_column("Offer")
        for key in cars_data[0]:
            self.add_column(key.title())

        for i, car in enumerate(cars_data, start=1):
            style = "green" if i % 2 == 0 else "blue"
            self.add_row(str(i), *car.values(), style=style)
