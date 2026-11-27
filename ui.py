from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import questionary
from questionary import Style
from contacts import Name, Phone, Birthday, Address, Email
from get_birthday import parse_days


# Повідомлення про успішні операції з контактами
SUCCESS_MESSAGES = {
    "Contact added.",
    "Contact updated.",
    "Phone updated.",
    "Birthday added.",
    "Email added.",
    "Address added.",
    "Contact deleted.",
}

# Попередження про відсутність даних контакту
WARNING_MESSAGES = {
    "No phone for this contact.",
    "Birthday not set for this contact.",
    "Email not set for this contact.",
    "Address not set for this contact.",
}

console = Console()

menu_style = Style([
    ("highlighted", "fg:#5fba9d bold"),
    ("pointer", "fg:#5fba9d bold"),
    ("answer", "fg:#5fba9d bold"),
])


# Форматує назву пункту меню та підказку команди
def menu_choice(title: str, command: str) -> questionary.Choice:
    return questionary.Choice(
        title=f"{title} ({command})",
        value=command
    )


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
            menu_choice("Add a contact", "add"),
            menu_choice("Show all contacts", "all"),
            menu_choice("Find a contact", "find"),
            menu_choice("Change phone", "change"),
            menu_choice("Show phone", "phone"),
            menu_choice("Add birthday", "add-birthday"),
            menu_choice("Show birthday", "show-birthday"),
            menu_choice("Upcoming birthdays", "birthdays"),
            menu_choice("Add email", "add-email"),
            menu_choice("Show email", "show-email"),
            menu_choice("Add address", "add-address"),
            menu_choice("Show address", "show-address"),
            menu_choice("Delete a contact", "delete"),
            menu_choice("Back to main menu", "back")
        ],
        style=menu_style,
        use_indicator=False
    ).ask()

# Відображає меню керування нотатками


def show_notes_menu() -> str | None:
    return questionary.select(
        "What would you like to do?",
        choices=[
            menu_choice("Add a note", "add"),
            menu_choice("Show all notes", "all"),
            menu_choice("Find a note by ID", "find"),
            menu_choice("Search notes", "search"),
            menu_choice("Edit a note", "edit"),
            menu_choice("Delete a note", "delete"),
            menu_choice("Delete all notes", "delete-all"),
            menu_choice("Add a tag", "add-tag"),
            menu_choice("Search by tag", "search-tag"),
            menu_choice("Sort by tags", "sort-tags"),
            menu_choice("Back to main menu", "back")
        ],
        style=menu_style,
        use_indicator=False
    ).ask()


# Запитує команду з автодоповненням
def get_command(commands: list[str]) -> str | None:
    return questionary.autocomplete(
        "Enter command:",
        choices=commands,
        ignore_case=True,
        style=menu_style,
        reserve_space_for_menu=10
    ).ask()


# Виводить повідомлення про успішну операцію
def show_success(message: str) -> None:
    console.print(f"✓ {message}\n", style="green", highlight=False)


# Виводить повідомлення про помилку
def show_error(message: str) -> None:
    console.print(f"✗ {message}\n", style="bold red", highlight=False)


# Виводить попередження
def show_warning(message: str) -> None:
    console.print(f"⚠ {message}\n", style="yellow", highlight=False)


# Виводить інформаційне повідомлення
def show_info(message: str) -> None:
    console.print(f"ℹ {message}\n", style="bold cyan", highlight=False)


# Запитує непорожнє значення
def get_required_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()

        if value:
            return value

        show_error("This field cannot be empty. Please try again.")


# Запитує значення та повторює введення у разі помилки валідації
def get_validated_input(prompt: str, validator, required: bool = True) -> str:
    while True:
        value = input(prompt).strip()

        if not value and not required:
            return ""

        try:
            validator(value)
            return value
        except ValueError as error:
            show_error(str(error))


# Запитує та перевіряє кількість днів
def get_birthday_days() -> str:
    return get_validated_input("\nEnter number of days: ", parse_days)


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
        box=box.ROUNDED,
        min_width=40
    )

    for header in headers:
        table.add_column(header)

    for row in rows:
        table.add_row(*row)

    console.print(table)


# =========================
# ХЕЛПЕРИ ВІДОБРАЖЕННЯ ТА ВВОДУ
# =========================

# Запитує та перевіряє аргументи для команд керування контактами
def get_contact_args(action: str, book) -> list[str] | None:
    name = get_validated_input("Enter contact name: ", Name)

    # Перевіряємо наявність контакту перед введенням інших даних
    if action != "add" and book.find(name) is None:
        show_error("Contact not found.")
        return None

    args = [name]

    prompts = {
        "add": ("Enter phone number (optional): ", Phone, False),
        "change": ("Enter new phone number: ", Phone, True),
        "add-birthday": ("Enter birthday (DD.MM.YYYY): ", Birthday, True),
        "add-email": ("Enter email: ", Email, True),
        "add-address": ("Enter address: ", Address, True),
    }

    if action in prompts:
        prompt_text, validator, required = prompts[action]
        value = get_validated_input(prompt_text, validator, required)

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
        title=f"\nUpcoming Birthdays · {days} days",
        headers=["#", "Name", "Birthday"],
        rows=rows,
        empty_message=f"No upcoming birthdays in the next {days} day(s).",
    )


# Відображає результат виконання команди для контактів
def show_contact_result(result: str) -> None:
    if result in SUCCESS_MESSAGES:
        show_success(result)
    elif result in WARNING_MESSAGES:
        show_warning(result)
    elif result in {"Contact not found", "Contact not found."}:
        show_error(result)
    else:
        console.print(result, markup=False)


# Пауза для користувача перед продовженням
def pause() -> None:
    input("\nPress Enter to continue...")
