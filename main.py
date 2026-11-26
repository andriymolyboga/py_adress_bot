from contact_commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    change_phone,
    delete_contact,
    find_contact,
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
    pause,
    show_contact_result,
    show_contacts_menu,
    show_error,
    show_info,
    show_main_menu,
    show_notes_menu,
    show_success,
    show_table,
    show_welcome,
)

# =========================
# ЦИКЛИ КЕРУВАННЯ РОЗДІЛАМИ
# =========================


def _run_section_loop(
    show_menu_func,
    handlers: dict,
    extra_commands: list[str],
    on_action,
) -> str | None:
    action = show_menu_func()

    while True:
        if action in {"back", None}:
            return None
        if action in {"exit", "close"}:
            return "exit"
        if action == "menu":
            action = show_menu_func()
            continue

        handled = on_action(action)
        if not handled:
            show_error("Unknown command.")

        pause()

        console.print(
            "\nType 'menu' to show actions, "
            "'back' for main menu, or 'exit' to quit.",
            style="dim",
        )

        next_action = get_command(list(handlers) + extra_commands)
        action = next_action.strip().lower() if next_action is not None else None


def manage_contacts(address_book) -> str | None:
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
        "find": find_contact,
        "delete": delete_contact,
    }

    def handle_contact_action(action: str) -> bool:
        if action == "hello":
            show_info("How can I help you?")
            return True

        if action == "all":
            display_contacts(address_book.data.values(), "My Contacts")
            return True

        if action == "find":
            name = get_required_input("Enter contact name: ")
            record = address_book.find(name)
            if record is None:
                show_error("Contact not found.")
            else:
                display_contacts([record], "Contact Details")
            return True

        # Окрема гілка для пошуку днів народження за задану кількість днів
        # Окрема гілка для пошуку днів народження за задану кількість днів
        if action == "birthdays":
            try:
                raw_days = get_birthday_days()
                days = parse_days(raw_days)
                upcoming = get_upcoming_birthdays_for_period(address_book, days)
                display_birthdays(upcoming, days)
            except BirthdayNotFoundError as error:
                show_info(str(error))
            except ValueError as error:
                show_error(str(error))
            return True

        if action in handlers:
            args = get_contact_args(action)
            result = handlers[action](args, address_book)
            show_contact_result(result)
            return True

        return False

    return _run_section_loop(
        show_menu_func=show_contacts_menu,
        handlers=handlers,
        extra_commands=["all", "birthdays", "menu", "back", "exit"],
        on_action=handle_contact_action,
    )


def manage_notes(notes_book: NotesBook) -> str | None:
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
        "sort-tags": sort_by_tags,
    }

    def handle_note_action(action: str) -> bool:
        if action in handlers:
            handlers[action](notes_book)
            return True
        return False

    return _run_section_loop(
        show_menu_func=show_notes_menu,
        handlers=handlers,
        extra_commands=["menu", "back", "exit"],
        on_action=handle_note_action,
    )


# =========================
# ГОЛОВНЕ МЕНЮ ПРОГРАМИ
# =========================


def _load_initial_state() -> tuple[object, NotesBook] | None:
    try:
        address_book = load_data()
    except (ValueError, OSError) as error:
        show_error(f"Could not load address book: {error}")
        return None

    try:
        notes_book = load_notes()
    except (ValueError, OSError) as error:
        show_error(f"Could not load notes: {error}")
        return None

    return address_book, notes_book


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
        elif choice in {"Exit", None}:
            break

    save_data(address_book)
    save_notes(notes_book)
    show_info("Address book and notes saved. Goodbye!")


# =========================
# ТОЧКА ВХОДУ
# =========================


if __name__ == "__main__":
    main()