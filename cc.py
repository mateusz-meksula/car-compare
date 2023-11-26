import asyncio

from app.functions import (
    get_cars_data,
    get_pages_contents,
    get_urls,
    make_report,
    show_report,
    show_welcome_message,
)


async def main():
    show_welcome_message()
    urls = get_urls()
    pages_contents = await get_pages_contents(urls)
    cars_data = get_cars_data(urls, pages_contents)
    report = make_report(cars_data)
    show_report(report)


if __name__ == "__main__":
    asyncio.run(main())
