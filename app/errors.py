from functools import partial

from rich import print


def print_error(text: str):
    print(f"[red]{text}")


def print_error_and_quit(text: str, *values):
    print_error(text.format(*values))
    quit()


invalid_url = partial(
    print_error,
    "Invalid url",
)


OffersNotAnInteger = partial(
    print_error_and_quit,
    """
Invalid input: [yellow]'{}'[/yellow]
Number of car offers must be an [bold]integer[/bold].
""",
)

OffersLessThat2 = partial(
    print_error_and_quit,
    """
Invalid input: [yellow]'{}'[/yellow]
Number of car offers must be an integer [bold]greater that 1[/bold].
""",
)

FetchFailed = partial(
    print_error_and_quit,
    """
Request to [yellow]'{}'[/yellow] failed.
Status code: [yellow]'{}'[/yellow].
""",
)

InvalidPageContent = partial(
    print_error_and_quit,
    """
Application was unable to obtain offer data from URL:
[white]'{}'[/white]
""",
)
