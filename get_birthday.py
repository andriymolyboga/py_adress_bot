from datetime import date, timedelta
from typing import Any


class BirthdayNotFoundError(ValueError):
    """Виникає, коли у вказаний період немає днів народження."""


def _is_leap_year(year: int) -> bool:
    """Перевіряє, чи є рік високосним."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _birthday_in_year(birth_date: date, target_year: int) -> date:
    """
    Повертає дату дня народження у вказаному році.
    Для 29 лютого у невисокосний рік повертає 28 лютого.
    """
    if birth_date.month == 2 and birth_date.day == 29 and not _is_leap_year(target_year):
        return date(target_year, 2, 28)
    return date(target_year, birth_date.month, birth_date.day)


def parse_days(raw_days: str, max_days: int = 3650) -> int:
    """Перевіряє та перетворює введений рядок у кількість днів."""
    cleaned = raw_days.strip()
    if not cleaned:
        raise ValueError("Number of days cannot be empty.")

    try:
        days = int(cleaned)
    except ValueError as exc:
        raise ValueError("Number of days must be an integer (e.g., 7, 14, 30).") from exc

    if days < 0:
        raise ValueError("Number of days cannot be negative.")

    if days > max_days:
        raise ValueError(f"Please enter a number of days no greater than {max_days}.")

    return days


def get_upcoming_birthdays_for_period(
    book: Any,
    days: int,
    reference_date: date | None = None,
) -> list[dict[str, str]]:
    """
    Повертає список контактів, у яких день народження потрапляє
    у проміжок [reference_date, reference_date + timedelta(days=days)].
    Піднімає BirthdayNotFoundError, якщо збігів немає.
    """
    days = parse_days(str(days))
    start_date = reference_date or date.today()
    end_date = start_date + timedelta(days=days)

    upcoming_birthdays: list[dict[str, str]] = []

    # Підтримуємо як AddressBook із .data, так і словник/об'єкт із .values()
    records = book.data.values() if hasattr(book, "data") else book.values()

    for record in records:
        if getattr(record, "birthday", None) is None or record.birthday.value is None:
            continue

        raw_bday = record.birthday.value
        birth_date = raw_bday.date() if hasattr(raw_bday, "date") else raw_bday

        # Перевіряємо поточний і наступний рік, щоб коректно обробити перехід через 31.12 -> 01.01
        candidate_dates = [
            _birthday_in_year(birth_date, start_date.year),
            _birthday_in_year(birth_date, start_date.year + 1),
        ]

        matching_birthday = next(
            (dt for dt in candidate_dates if start_date <= dt <= end_date),
            None,
        )

        if matching_birthday is not None:
            upcoming_birthdays.append({
                "name": record.name.value,
                "birthday": matching_birthday.strftime("%d.%m.%Y"),
            })

    if not upcoming_birthdays:
        raise BirthdayNotFoundError(f"No upcoming birthdays in the next {days} day(s).")

    upcoming_birthdays.sort(key=lambda item: tuple(map(int, item["birthday"].split(".")[::-1])))
    return upcoming_birthdays


def format_birthdays_output(birthdays: list[dict[str, str]], days: int) -> str:
    """Форматує результат для виводу в консольному боті."""
    if not birthdays:
        return f"No upcoming birthdays in the next {days} day(s)."

    lines = [f"Upcoming birthdays in the next {days} day(s):"]
    for entry in birthdays:
        lines.append(f"- {entry['name']}: {entry['birthday']}")

    return "\n".join(lines)


def handle_get_birthday(args: list[str], book: Any) -> str:
    """
    Хендлер для підключення до командного меню бота.
    Підтримує виклик як із аргументом (наприклад: `birthdays 14`),
    так і з інтерактивним запитом кількості днів.
    """
    if args:
        raw_days = args[0]
    else:
        raw_days = input("Enter the number of days to search for birthdays: ")

    days = parse_days(raw_days)
    matches = get_upcoming_birthdays_for_period(book, days)
    return format_birthdays_output(matches, days)