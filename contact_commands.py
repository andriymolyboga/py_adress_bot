from contacts import AddressBook, Record


# =========================
# ОБРОБКА ПОМИЛОК
# =========================

def input_error(func):
    # Декоратор без wraps перехоплює типові помилки вводу та повертає зрозуміле повідомлення
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not found"

    return inner

# =========================
# КОМАНДИ ДЛЯ ТЕЛЕФОНІВ І КОНТАКТІВ
# =========================

@input_error
def add_contact(args, book: AddressBook):
    # Створює новий контакт або оновлює телефон існуючого
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: AddressBook):
    # Оновлює єдиний номер телефону контакту
    name, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.edit_phone(new_phone)
    return "Phone updated."


@input_error
def show_phones(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    if record.phone is None:
        return "No phone for this contact."
    return str(record.phone)


# =========================
# КОМАНДИ ДЛЯ ДНЯ НАРОДЖЕННЯ
# =========================

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    if record.birthday is None:
        return "Birthday not set for this contact."
    return str(record.birthday)


# =========================
# КОМАНДИ ДЛЯ EMAIL ТА АДРЕСИ
# =========================

@input_error
def add_email(args, book: AddressBook):
    # Валідація формату відбувається всередині Email -> Record.add_email
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.add_email(email)
    return "Email added."


@input_error
def show_email(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    if record.email is None:
        return "Email not set for this contact."
    return str(record.email)


@input_error
def add_address(args, book: AddressBook):
    # Об'єднуємо всі слова після імені, щоб коректно зберегти адресу з пробілами
    name = args[0]
    if len(args) < 2:
        raise IndexError
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    record.add_address(address)
    return "Address added."


@input_error
def show_address(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found")
    if record.address is None:
        return "Address not set for this contact."
    return str(record.address)

# =========================
# ПОШУК ТА ВИДАЛЕННЯ КОНТАКТІВ
# =========================

@input_error
def find_contact(args, book: AddressBook):
    # Шукає контакт за іменем через наявний метод AddressBook.find
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found"
    return str(record)


@input_error
def delete_contact(args, book: AddressBook):
    # Видаляє контакт за іменем через наявний метод AddressBook.delete
    name = args[0]
    book.delete(name)
    return "Contact deleted."


# =========================
# ПЕРЕГЛЯД УСІХ КОНТАКТІВ
# =========================

@input_error
def show_all(book: AddressBook):
    return str(book)