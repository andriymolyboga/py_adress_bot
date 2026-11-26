from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import questionary
from questionary import Style


console = Console()

menu_style = Style([
    ("highlighted", "fg:#5fba9d bold"),
    ("pointer", "fg:#5fba9d bold"),
])

# Відображає привітальний екран застосунку
def show_welcome() -> None:
    console.print(
        Panel(
            "[bold gold1]Personal Assistant[/bold gold1]\n\n"
            "Organize your contacts. Capture your thoughts.",
            border_style="dark_orange3",
            box=box.ROUNDED,
            padding=(1, 2),
            width=60
        )
    )


# Відображає головне меню
def show_main_menu() -> str | None:
    return questionary.select(
        "What would you like to work with?",
        choices=["Contacts", "Notes", "Exit"],
        style=menu_style,
        use_indicator=False
    ).ask()


# Відображає меню керування нотатками
def show_notes_menu() -> str | None:
    return questionary.select(
        "What would you like to do?",
        choices=[
            questionary.Choice("Add a note (add)", value="add"),
            questionary.Choice("Show all notes (all)", value="all"),
            questionary.Choice("Find a note by ID (find)", value="find"),
            questionary.Choice("Search notes (search)", value="search"),
            questionary.Choice("Edit a note (edit)", value="edit"),
            questionary.Choice("Delete a note (delete)", value="delete"),
            questionary.Choice("Delete all notes (delete-all)", value="delete-all"),
            questionary.Choice("Add a tag (add-tag)", value="add-tag"),
            questionary.Choice("Search by tag (search-tag)", value="search-tag"),
            questionary.Choice("Sort by tags (sort-tags)", value="sort-tags"),
            questionary.Choice("Back to main menu (back)", value="back")
        ],
        style=menu_style,
        use_indicator=False
    ).ask()


# Запитує команду з автодоповненням
def get_command(commands: list[str]) -> str | None:
    return questionary.autocomplete(
        "Enter command:",
        choices=commands,
        ignore_case=True
    ).ask()


# Виводить повідомлення про успішну операцію
def show_success(message: str) -> None:
    console.print(f"\n✓ {message}", style="green")


# Виводить повідомлення про помилку
def show_error(message: str) -> None:
    console.print(f"\n✗ {message}", style="bold red")


# Виводить попередження
def show_warning(message: str) -> None:
    console.print(f"\n⚠ {message}", style="yellow")


# Виводить інформаційне повідомлення
def show_info(message: str) -> None:
    console.print(f"\nℹ {message}", style="bold cyan")

# Запитує непорожнє значення
def get_required_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()

        if value:
            return value

        show_error("This field cannot be empty. Please try again.")


# Виводить дані у вигляді таблиці
def show_table(
    title: str,
    headers: list[str],
    rows: list[list[str]]
) -> None:

    if not rows:
        show_warning("No records found.")
        return

    table = Table(
        title=title,
        title_style="bold gold1",
        header_style="bold wheat1",
        border_style="dark_orange3",
        show_lines=True,
        box=box.ROUNDED
    )

    for header in headers:
        table.add_column(header)

    for row in rows:
        table.add_row(*row)

    console.print(table)
