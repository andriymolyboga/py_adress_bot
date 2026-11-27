import csv
from pathlib import Path

from notes import Note, NotesBook

DEFAULT_NOTES_FILE = Path(__file__).parent / "data" / "notes.csv"
FIELDNAMES = ["id", "title", "text", "tags"]


def _serialize_tags(tags: set[str]) -> str:
    # Зберігаємо множину тегів у стабільному порядку через крапку з комою
    return ";".join(sorted(tags))


def _deserialize_tags(raw_tags: str | None) -> set[str]:
    if not raw_tags:
        return set()
    return {tag.strip().lower() for tag in raw_tags.split(";") if tag.strip()}


def save_notes(
    notes_book: NotesBook,
    filename: Path = DEFAULT_NOTES_FILE
) -> None:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for note in notes_book.data.values():
            writer.writerow({
                "id": note.id,
                "title": note.title,
                "text": note.text,
                "tags": _serialize_tags(note.tags),
            })


def load_notes(filename: Path = DEFAULT_NOTES_FILE) -> NotesBook:
    path = Path(filename)
    book = NotesBook()

    if not path.exists():
        return book

    max_id = 0

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, strict=True)

        # Перевіряємо структуру CSV-файлу
        if reader.fieldnames != FIELDNAMES:
            raise ValueError("Invalid notes CSV headers.")

        for row_number, row in enumerate(reader, start=2):
            # Перевіряємо кількість полів у рядку
            if None in row or None in row.values():
                raise ValueError(
                    f"Invalid notes CSV structure at row {row_number}."
                )

            raw_id = (row.get("id") or "").strip()
            title = (row.get("title") or "").strip()
            text = (row.get("text") or "").strip()
            tags = _deserialize_tags(row.get("tags"))

            # Перевіряємо обов'язкові поля нотатки
            if not raw_id or not title or not text:
                raise ValueError(
                    f"Missing required note fields at row {row_number}."
                )

            note_id = int(raw_id)
            note = Note(note_id=note_id, title=title, text=text, tags=tags)
            book.data[note.id] = note

            if note.id > max_id:
                max_id = note.id

    # Щоб нові нотатки після перезапуску не перетирали існуючі ID
    book.next_id = max_id + 1
    return book
