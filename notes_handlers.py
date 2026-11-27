from notes import Note, NotesBook
from ui import (
    show_table,
    show_success,
    show_error,
    show_warning,
    get_required_input,
    get_input,
    show_info
)


# Відображення списку нотаток у вигляді таблиці
def display_notes(notes: list[Note], title: str) -> None:
    rows = []

    for note in notes:
        if note.tags:
            tags = ", ".join(sorted(note.tags))
        else:
            tags = "-"

        rows.append([str(note.id), note.title, note.text, tags])

    show_table(
        title=title,
        headers=["ID", "Title", "Text", "Tags"],
        rows=rows
    )


# Запит підтвердження дії користувачем
def confirm_action(prompt: str) -> bool:
    confirmation = get_input(prompt).lower()
    return confirmation in ["y", "yes"]


# Додавання нової нотатки
def add_note(book: NotesBook) -> None:
    title = get_required_input("\nEnter note title: ")
    text = get_required_input("Enter note text: ")

    try:
        note = book.add_note(title, text)
        show_success(f"Note added successfully. ID: {note.id}")

    except ValueError as error:
        show_error(str(error))


# Відображення всіх збережених нотаток
def show_all_notes(book: NotesBook) -> None:
    display_notes(book.all_notes(), "\nMy Notes")


# Виведення нотатки за її ID
def show_note(book: NotesBook) -> None:
    try:
        note_id = int(get_required_input("Enter note ID: "))
    except ValueError:
        show_error("ID must be an integer.")
        return

    note = book.find_note(note_id)

    if note is None:
        show_error("Note not found.")
        return

    display_notes([note], "\nNote Details")


# Пошук нотатки за назвою або текстом
def search_notes(book: NotesBook) -> None:
    query = get_required_input("Enter search query: ")
    notes = book.search_notes(query)

    display_notes(notes, "\nSearch Results")


# Редагування назви та/або тексту нотатки
def edit_note(book: NotesBook) -> None:

    try:
        note_id = int(get_required_input("\nEnter note ID: "))
    except ValueError:
        show_error("ID must be an integer.")
        return

    note = book.find_note(note_id)

    if note is None:
        show_error("Note not found.")
        return

    display_notes([note], "\nCurrent Note")

    show_info("Press Enter to keep the current value.")

    title = get_input("\nEnter new title: ")
    text = get_input("Enter new text: ")

    if not title and not text:
        show_warning("No changes made.")
        return

    book.edit_note(note_id, title, text)
    show_success("Note updated successfully.")


# Видалення нотатки за ID
def delete_note(book: NotesBook) -> None:

    try:
        note_id = int(get_required_input("Enter note ID: "))
    except ValueError:
        show_error("ID must be an integer.")
        return

    note = book.find_note(note_id)

    if note is None:
        show_error("Note not found.")
        return

    display_notes([note], "\nNote to Delete")

    if confirm_action("\nDelete this note? (yes/no): "):
        book.delete_note(note_id)
        show_success("Note deleted successfully.")
    else:
        show_info("Deletion cancelled.")


# Видалення всіх нотаток з підтвердженням
def delete_all_notes(book: NotesBook) -> None:

    if not book:
        show_warning("No notes to delete.")
        return

    show_all_notes(book)

    show_warning(f"You are about to delete all {len(book)} notes.")

    if confirm_action("\nDelete all notes? (yes/no): "):
        deleted_count = book.delete_all_notes()
        show_success(f"All {deleted_count} notes deleted successfully.")
    else:
        show_info("Deletion cancelled.")


# Додавання тегу до наявної нотатки
def add_tag(book: NotesBook) -> None:

    try:
        note_id = int(get_required_input("\nEnter note ID: "))
    except ValueError:
        show_error("ID must be an integer.")
        return

    note = book.find_note(note_id)

    if note is None:
        show_error("Note not found.")
        return

    display_notes([note], "\nCurrent Note")

    tag = get_required_input("\nEnter new tag: ")

    book.add_tag(note_id, tag)
    show_success("Tag added successfully.")


# Пошук нотаток за тегом
def search_by_tag(book: NotesBook) -> None:
    tag = get_required_input("\nEnter tag to search: ")
    notes = book.search_by_tag(tag)

    display_notes(notes, "\nSearch Results by Tag")


# Відображення нотаток, відсортованих за тегами
def sort_by_tags(book: NotesBook) -> None:
    sorted_notes = book.sort_by_tags()
    display_notes(sorted_notes, "\nMy Notes Sorted by Tags")
