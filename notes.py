from collections import UserDict
from ui import show_table


class Note:
    def __init__(
        self,
        note_id: int,
        title: str,
        text: str,
        tags: set[str] | None = None
    ):
        self.id = note_id
        self.title = title
        self.text = text
        self.tags = set()

        if tags:
            for tag in tags:
                self.add_tag(tag)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value.strip():
            raise ValueError("Title cannot be empty.")
        self._title = value.strip()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value.strip():
            raise ValueError("Text cannot be empty.")
        self._text = value.strip()

    # Додає тег до нотатки
    def add_tag(self, tag: str) -> None:
        tag = tag.strip().lower()
        if not tag:
            raise ValueError("Tag cannot be empty.")
        self.tags.add(tag)

    def __str__(self):
        return f"ID: {self.id}\nTitle: {self.title}\nText: {self.text}"


class NotesBook(UserDict):
    def __init__(self):
        super().__init__()
        self.next_id = 1

    # Додає нотатки до списку нотатків
    def add_note(self, title: str, text: str, tags: set[str] | None = None):
        note = Note(self.next_id, title, text, tags)
        self.data[note.id] = note
        self.next_id += 1
        return note

    # Шукає нотатку за ID
    def find_note(self, note_id: int) -> Note | None:
        return self.data.get(note_id)

    # Додає тег до наявної нотатки
    def add_tag(self, note_id: int, tag: str) -> bool:

        note = self.find_note(note_id)

        if note is None:
            return False

        note.add_tag(tag)
        return True

    # Шукає нотатки за назвою або текстом
    def search_notes(self, query: str) -> list[Note]:
        note_list = []
        query = query.lower()

        for note in self.data.values():
            if query in note.title.lower() or query in note.text.lower():
                note_list.append(note)

        return note_list

    # Шукає нотатки за тегом
    def search_by_tag(self, tag: str) -> list[Note]:
        note_tag_list = []
        tag = tag.strip().lower()

        for note in self.data.values():
            if tag in note.tags:
                note_tag_list.append(note)

        return note_tag_list

    # Сортує нотатки за тегами
    def sort_by_tags(self) -> list[Note]:
        return sorted(
            self.data.values(),
            key=lambda note: (not note.tags, sorted(note.tags))
        )

    # Видаляє нотатку за ID
    def delete_note(self, note_id: int) -> bool:

        if note_id in self.data:
            self.data.pop(note_id)
            return True
        return False

    # Змінює назву та/або текст нотатки
    def edit_note(
        self,
        note_id: int,
        title: str | None = None,
        text: str | None = None
    ) -> bool:

        note = self.find_note(note_id)

        if note is None:
            return False

        if title and title.strip():
            note.title = title

        if text and text.strip():
            note.text = text

        return True

    # Повертає всі збережені нотатки
    def all_notes(self) -> list[Note]:
        return list(self.data.values())

    # Видаляє всі нотатки та повертає їх кількість
    def delete_all_notes(self) -> int:

        all_notes = len(self.data)
        self.data.clear()
        return all_notes
