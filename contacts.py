from datetime import datetime
import re


# =========================
# БАЗОВИЙ КЛАС ПОЛЯ
# =========================

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# =========================
# КЛАСИ ПОЛІВ КОНТАКТУ
# =========================

class Name(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty")

        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value):
        value = str(value).strip()

        if not value.isdigit():
            raise ValueError("Phone must contain only digits")

        if len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits")

        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
        except (ValueError, TypeError):
            raise ValueError(
                "Invalid birthday format. Use DD.MM.YYYY"
            )

        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Address(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Address cannot be empty")

        super().__init__(value.strip())


class Email(Field):
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Email must be a string")

        value = value.strip()
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(pattern, value):
            raise ValueError("Invalid email format")

        super().__init__(value)


# =========================
# ЗАПИС КОНТАКТУ
# =========================

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = None
        self.birthday = None
        self.address = None
        self.email = None

    def add_phone(self, phone):
        # Зберігає або оновлює єдиний номер телефону контакту
        self.phone = Phone(phone)

    def remove_phone(self):
        if self.phone is None:
            raise ValueError("Phone not found")
        self.phone = None

    def edit_phone(self, new_phone):
        if self.phone is None:
            raise ValueError("Phone not found")
        self.phone = Phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def __str__(self):
        parts = [f"Contact name: {self.name.value}"]

        if self.phone:
            parts.append(f"phone: {self.phone}")

        if self.birthday:
            parts.append(f"birthday: {self.birthday}")

        if self.address:
            parts.append(f"address: {self.address}")

        if self.email:
            parts.append(f"email: {self.email}")

        return ", ".join(parts)


# =========================
# АДРЕСНА КНИГА
# =========================

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name not in self.data:
            raise ValueError("Contact not found")

        del self.data[name]

    def __str__(self):
        if not self.data:
            return "Address book is empty"

        return "\n".join(
            str(record) for record in self.data.values()
        )