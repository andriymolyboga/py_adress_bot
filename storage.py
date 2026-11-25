import csv
from pathlib import Path

from contacts import AddressBook, Record


# =========================
# НАЛАШТУВАННЯ ФАЙЛУ
# =========================

DATA_FILE = Path(__file__).parent / "data" / "addressbook.csv"


# =========================
# ЗБЕРЕЖЕННЯ АДРЕСНОЇ КНИГИ
# =========================

def save_data(book, filename=DATA_FILE):
    filename = Path(filename)

    # Створюємо папку, якщо її немає
    filename.parent.mkdir(parents=True, exist_ok=True)

    with filename.open("w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "phone", "birthday", "email", "address"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for record in book.data.values():
            writer.writerow({
                "name": record.name.value,
                "phone": record.phone.value if record.phone else "",
                "birthday": (
                    record.birthday.value.strftime("%d.%m.%Y")
                    if record.birthday else ""
                ),
                "email": record.email.value if record.email else "",
                "address": record.address.value if record.address else "",
            })


# =========================
# ЗАВАНТАЖЕННЯ АДРЕСНОЇ КНИГИ
# =========================

def load_data(filename=DATA_FILE):
    filename = Path(filename)

    book = AddressBook()

    # Якщо файл ще не існує, повертаємо порожню книгу
    if not filename.exists():
        return book

    with filename.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            try:
                record = Record(row["name"])

                if row.get("phone"):
                    record.add_phone(row["phone"])

                if row.get("birthday"):
                    record.add_birthday(row["birthday"])

                if row.get("email"):
                    record.add_email(row["email"])

                if row.get("address"):
                    record.add_address(row["address"])

                book.add_record(record)

            except (ValueError, KeyError, TypeError) as error:
                raise ValueError(
                    f"Error loading contact at CSV row "
                    f"{row_number}: {error}"
                ) from error

    return book