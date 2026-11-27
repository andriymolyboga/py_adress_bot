from difflib import get_close_matches
from contact_commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    change_phone,
    delete_contact,
    show_address,
    show_birthday,
    show_email,
    show_phones,
)
from get_birthday import (
    BirthdayNotFoundError,
    get_upcoming_birthdays_for_period,
    parse_days,
)
from notes import NotesBook
from notes_handlers import (
    add_note,
    add_tag,
    delete_all_notes,
    delete_note,
    edit_note,
    search_by_tag,
    search_notes,
    show_all_notes,
    show_note,
    sort_by_tags,
)
from notes_storage import load_notes, save_notes
from storage import load_data, save_data
from ui import (
    console,
    display_birthdays,
    display_contacts,
    get_birthday_days,
    get_command,
    get_contact_args,
    get_required_input,
    show_contact_result,
    show_contacts_menu,
    show_error,
    show_info,
    show_main_menu,
    show_notes_menu,
    show_welcome,
    show_warning
)


# =========================
# НАВІГАЦІЯ МІЖ РОЗДІЛАМИ
# =========================

# Забезпечує спільну логіку навігації та обробки команд
def _run_section_loop(
    show_menu_func,
    handlers: dict,
    extra_commands: list[str],
    on_action,
) -> str | None:
    action = show_menu_func()

    while True:
        if action == "menu":
            action = show_menu_func()
            continue

        elif action == "back" or action is None:
            return

        elif action in ("exit", "close"):
            return "exit"

        elif not on_action(action):
            # Шукаємо найближчу команду у разі помилки введення
            matches = get_close_matches(
                action,
                list(handlers) + extra_commands,
                n=1,
                cutoff=0.6
            )

            if matches:
                show_warning(f"Unknown command. Did you mean '{matches[0]}'?")
            else:
                show_error("Unknown command.")

        console.print(
            "\nType 'menu' to show actions, "
            "'back' for main menu, or 'exit' to quit.",
            style="dim"
        )

        # Отримуємо наступну команду з автодоповненням
        action = get_command(
            list(handlers) + extra_commands
        )

        if action is not None:
            action = action.strip().lower()


# =========================
# КЕРУВАННЯ НОТАТКАМИ
# =========================

# Керує командами для роботи з нотатками та тегами
def manage_notes(notes_book: NotesBook) -> str | None:

    # Словник доступних команд та відповідних функцій
    handlers = {
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

    # Виконує вибрану команду для книги нотаток
    def handle_note_action(action: str) -> bool:
        if action in handlers:
            handlers[action](notes_book)
            return True

        return False

    # Запускаємо спільний цикл навігації для нотаток
    return _run_section_loop(
        show_menu_func=show_notes_menu,
        handlers=handlers,
        extra_commands=["menu", "back", "exit"],
        on_action=handle_note_action,
    )


# =========================
# КЕРУВАННЯ КОНТАКТАМИ
# =========================

# Керує командами для роботи з адресною книгою
def manage_contacts(book) -> str | None:

    # Словник доступних команд та відповідних функцій
    handlers = {
        "add": add_contact,
        "change": change_phone,
        "phone": show_phones,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "add-email": add_email,
        "show-email": show_email,
        "add-address": add_address,
        "show-address": show_address,
        "delete": delete_contact
    }

    # Обробляє вибрану команду для адресної книги
    def handle_contact_action(action: str) -> bool:

        if action == "all":
            display_contacts(book.data.values(), "My Contacts")

        elif action == "find":
            name = get_required_input("Enter contact name: ")
            record = book.find(name)

            if record is None:
                show_error("Contact not found.")
            else:
                display_contacts([record], "Contact Details")

        elif action == "birthdays":
            try:
                raw_days = get_birthday_days()
                days = parse_days(raw_days)
                upcoming = get_upcoming_birthdays_for_period(book, days)
                display_birthdays(upcoming, days)

            except BirthdayNotFoundError as error:
                show_info(str(error))

            except ValueError as error:
                show_error(str(error))

        elif action in handlers:
            args = get_contact_args(action, book)

            if args is not None:
                result = handlers[action](args, book)
                show_contact_result(result)

        elif action == "hello":
            show_info("How can I help you?")

        else:
            return False

        return True

    # Запускаємо спільний цикл навігації для контактів
    return _run_section_loop(
        show_menu_func=show_contacts_menu,
        handlers=handlers,
        extra_commands=[
            "all", "find", "birthdays",
            "menu", "back", "exit"
        ],
        on_action=handle_contact_action,
    )


# =========================
# ГОЛОВНЕ МЕНЮ ПРОГРАМИ
# =========================

# Завантажує збережені контакти та нотатки під час запуску
def _load_initial_state() -> tuple[object, NotesBook] | None:

    # Завантажуємо адресну книгу
    try:
        address_book = load_data()
    except (ValueError, OSError) as error:
        show_error(f"Could not load address book: {error}")
        return None

    # Завантажуємо книгу нотаток
    try:
        notes_book = load_notes()
    except (ValueError, OSError) as error:
        show_error(f"Could not load notes: {error}")
        return None

    return address_book, notes_book


# Керує життєвим циклом застосунку
def main() -> None:
    state = _load_initial_state()

    if state is None:
        return

    address_book, notes_book = state

    show_welcome()

    while True:
        choice = show_main_menu()

        if choice == "Contacts":
            if manage_contacts(address_book) == "exit":
                break

        elif choice == "Notes":
            if manage_notes(notes_book) == "exit":
                break

        elif choice == "Exit" or choice is None:
            break

    # Зберігаємо контакти та нотатки перед завершенням роботи
    try:
        save_data(address_book)
        save_notes(notes_book)
        show_info("Contacts and notes saved. Goodbye!")

    except (ValueError, OSError) as error:
        show_error(f"Could not save data: {error}")


# =========================
# ТОЧКА ВХОДУ
# =========================

# Запускаємо застосунок при безпосередньому виконанні файлу
if __name__ == "__main__":
    main()
