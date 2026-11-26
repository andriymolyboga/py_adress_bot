from contact_commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    change_phone,
    show_address,
    show_birthday,
    show_email,
    show_phones,
    find_contact,
    delete_contact,
)
from storage import load_data, save_data

from notes import NotesBook
from notes_handlers import (
    add_note,
    show_all_notes,
    show_note,
    search_notes,
    edit_note,
    delete_note,
    delete_all_notes,
    add_tag,
    search_by_tag,
    sort_by_tags
)

from ui import (
    console,
    show_welcome,
    show_main_menu,
    show_notes_menu,
    get_command,
    show_error,
    show_info,
    show_contacts_menu,
    get_required_input,
    show_table,
    show_success
)


# =========================
# КЕРУВАННЯ НОТАТКАМИ
# =========================

def manage_notes(notes_book):

    commands = {
        "add": add_note,
        "all": show_all_notes,
        "find": show_note,
        "search": search_notes,
        "edit": edit_note,
        "delete": delete_note,
        "delete-all": delete_all_notes,
        "add-tag": add_tag,
        "search-tag": search_by_tag,
        "sort-tags": sort_by_tags
    }

    action = show_notes_menu()

    while True:
        if action in commands:
            function = commands[action]
            function(notes_book)

        elif action == "menu":
            action = show_notes_menu()
            continue

        elif action == "back" or action is None:
            return

        elif action == "exit":
            return "exit"

        else:
            show_error("Unknown command.")

        console.print(
            "\nType 'menu' to show actions, "
            "'back' for main menu, or 'exit' to quit.",
            style="dim"
        )

        action = get_command(
            list(commands) + ["menu", "back", "exit"]
        )

        if action is not None:
            action = action.strip().lower()


# =========================
# КЕРУВАННЯ КОНТАКТАМИ
# =========================

# Запитує аргументи для команд керування контактами
def get_contact_args(action: str) -> list[str]:
    name = get_required_input("Enter contact name: ")
    args = [name]

    if action == "add":
        phone = input("Enter phone number (optional): ").strip()
        if phone:
            args.append(phone)

    elif action == "change":
        phone = get_required_input("Enter new phone number: ")
        args.append(phone)

    elif action == "add-birthday":
        birthday = get_required_input("Enter birthday (DD.MM.YYYY): ")
        args.append(birthday)

    elif action == "add-email":
        email = get_required_input("Enter email: ")
        args.append(email)

    elif action == "add-address":
        address = get_required_input("Enter address: ")
        args.append(address)

    return args


# Відображення контактів у вигляді таблиці
def display_contacts(contacts, title: str) -> None:
    rows = []

    for record in contacts:
        rows.append([
            str(record.name),
            str(record.phone) if record.phone else "-",
            str(record.birthday) if record.birthday else "-",
            str(record.email) if record.email else "-",
            str(record.address) if record.address else "-"
        ])

    show_table(
        title=title,
        headers=["Name", "Phone", "Birthday", "Email", "Address"],
        rows=rows
    )


# Відображає результат виконання команди
def show_contact_result(result: str) -> None:
    success_messages = [
        "Contact added.",
        "Contact updated.",
        "Phone updated.",
        "Birthday added.",
        "Email added.",
        "Address added.",
        "Contact deleted."
    ]

    if result in success_messages:
        show_success(result)
    else:
        console.print(result, markup=False)


def manage_contacts(book):

    commands = {
        "add": add_contact,
        "change": change_phone,
        "phone": show_phones,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "add-email": add_email,
        "show-email": show_email,
        "add-address": add_address,
        "show-address": show_address,
        "find": find_contact,
        "delete": delete_contact
    }

    action = show_contacts_menu()

    while True:
        if action == "all":
            display_contacts(book.data.values(), "My Contacts")

        elif action == "find":
            name = get_required_input("Enter contact name: ")
            record = book.find(name)

            if record is None:
                show_error("Contact not found.")
            else:
                display_contacts([record], "Contact Details")

        elif action in commands:
            args = get_contact_args(action)

            function = commands[action]
            result = function(args, book)
            show_contact_result(result)

        elif action == "menu":
            action = show_contacts_menu()
            continue

        elif action == "back" or action is None:
            return

        elif action in ("exit", "close"):
            return "exit"

        elif action == "hello":
            show_info("How can I help you?")

        else:
            show_error("Unknown command.")

        console.print(
            "\nType 'menu' to show actions, "
            "'back' for main menu, or 'exit' to quit.",
            style="dim"
        )

        action = get_command(
            list(commands) + ["all", "menu", "back", "exit"]
        )

        if action is not None:
            action = action.strip().lower()


# =========================
# ГОЛОВНЕ МЕНЮ ПРОГРАМИ
# =========================

def main():

    # Завантажуємо адресну книгу
    try:
        book = load_data()
    except (ValueError, OSError) as error:
        show_error(f"Could not load address book: {error}")
        return

    # Створюємо книгу нотаток
    notes_book = NotesBook()

    show_welcome()

    while True:
        choice = show_main_menu()

        if choice == "Contacts":
            if manage_contacts(book) == "exit":
                break

        elif choice == "Notes":
            if manage_notes(notes_book) == "exit":
                break

        elif choice == "Exit" or choice is None:
            break

    # Зберігаємо адресну книгу
    save_data(book)
    show_info("Address book saved. Goodbye!")


# =========================
# ТОЧКА ВХОДУ
# =========================

if __name__ == "__main__":
    main()