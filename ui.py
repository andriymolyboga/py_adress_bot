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


# Відображає меню керування контактами
def show_contacts_menu() -> str | None:
    return questionary.select(
        "What would you like to do?",
        choices=[
            questionary.Choice("Add a contact (add)", value="add"),
            questionary.Choice("Show all contacts (all)", value="all"),
            questionary.Choice("Find a contact (find)", value="find"),
            questionary.Choice("Change phone (change)", value="change"),
            questionary.Choice("Show phone (phone)", value="phone"),
            questionary.Choice("Add birthday (add-birthday)", value="add-birthday"),
            questionary.Choice("Show birthday (show-birthday)", value="show-birthday"),
            questionary.Choice("Upcoming birthdays (birthdays)", value="birthdays"),
            questionary.Choice("Add email (add-email)", value="add-email"),
            questionary.Choice("Show email (show-email)", value="show-email"),
            questionary.Choice("Add address (add-address)", value="add-address"),
            questionary.Choice("Show address (show-address)", value="show-address"),
            questionary.Choice("Delete a contact (delete)", value="delete"),
            questionary.Choice("Back to main menu (back)", value="back")
        ],
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


# Запитує кількість днів для пошуку днів народження
def get_birthday_days() -> str:
    return get_required_input("Enter number of days: ")


# Виводить дані у вигляді таблиці
def show_table(
    title: str,
    headers: list[str],
    rows: list[list[str]],
    empty_message: str = "No records found."
) -> None:
    if not rows:
        show_warning(empty_message)
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


# =========================
# ХЕЛПЕРИ ВІДОБРАЖЕННЯ ТА ВВОДУ
# =========================

def get_contact_args(action: str) -> list[str]:
    name = get_required_input("Enter contact name: ")
    args = [name]

    prompts = {
        "add": ("Enter phone number (optional): ", False),
        "change": ("Enter new phone number: ", True),
        "add-birthday": ("Enter birthday (DD.MM.YYYY): ", True),
        "add-email": ("Enter email: ", True),
        "add-address": ("Enter address: ", True),
    }

    if action in prompts:
        prompt_text, required = prompts[action]
        value = get_required_input(prompt_text) if required else input(prompt_text).strip()
        if value:
            args.append(value)

    return args


def display_contacts(contacts, title: str) -> None:
    rows = [
        [
            str(record.name),
            str(record.phone) if record.phone else "-",
            str(record.birthday) if record.birthday else "-",
            str(record.email) if record.email else "-",
            str(record.address) if record.address else "-",
        ]
        for record in contacts
    ]

    show_table(
        title=title,
        headers=["Name", "Phone", "Birthday", "Email", "Address"],
        rows=rows,
    )


# Виводить список найближчих днів народження у вигляді таблиці
def display_birthdays(birthdays: list[dict[str, str]], days: int) -> None:
    rows = [
        [
            str(index),
            entry["name"],
            entry["birthday"],
        ]
        for index, entry in enumerate(birthdays, start=1)
    ]

    show_table(
        title=f"Upcoming Birthdays (Next {days} Day(s))",
        headers=["#", "Name", "Birthday"],
        rows=rows,
        empty_message=f"No upcoming birthdays in the next {days} day(s).",
    )


def show_contact_result(result: str) -> None:
    if result in SUCCESS_MESSAGES:
        show_success(result)
    elif result in {"Contact not found", "Contact not found."}:
        show_error(result)
    else:
        console.print(result, markup=False)


# Пауза для користувача перед продовженням
def pause() -> None:
    input("\nPress Enter to continue...")
