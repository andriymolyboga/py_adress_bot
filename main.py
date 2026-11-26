from contacts import AddressBook
from contact_commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    change_phone,
    show_address,
    show_all,
    show_birthday,
    show_email,
    show_phones,
    find_contact,
    delete_contact,
)
from storage import load_data, save_data

# =========================
# ОБРОБКА КОМАНД
# =========================

def parse_input(user_input):
    """
    Розділяє введену команду та її аргументи.
    """
    parts = user_input.strip().split()

    if not parts:
        return None, []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


# =========================
# ГОЛОВНИЙ ЦИКЛ ПРОГРАМИ
# =========================

def main():

    # Завантажуємо адресну книгу
    try:
        book = load_data()
    except (ValueError, OSError) as error:
        print(f"Не вдалося завантажити адресну книгу: {error}")
        return

    print("Вітаю! Я ваш персональний помічник.")
    print("Введіть команду для роботи з адресною книгою.")

    while True:
        user_input = input("Введіть команду: ")

        command, args = parse_input(user_input)

        if command is None:
            continue

        # Вихід із програми
        if command in ["close", "exit"]:
            save_data(book)
            print("Адресну книгу збережено. До побачення!")
            break

        # Привітання
        elif command == "hello":
            print("Чим можу допомогти?")

        # Додавання контакту або оновлення телефону
        elif command == "add":
            print(add_contact(args, book))

        # Зміна номера телефону
        elif command == "change":
            print(change_phone(args, book))

        # Пошук номера телефону
        elif command == "phone":
            print(show_phones(args, book))

        # День народження
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "birthday":
            print(show_birthday(args, book))

        # Email
        elif command == "add-email":
            print(add_email(args, book))

        elif command == "email":
            print(show_email(args, book))

        # Адреса
        elif command == "add-address":
            print(add_address(args, book))

        elif command == "address":
            print(show_address(args, book))

        # Виведення всіх контактів
        elif command == "all":
            print(show_all(book))

        # Пошук контакту за іменем
        elif command == "find":
            print(find_contact(args, book))

        # Видалення контакту за іменем
        elif command == "delete":
            print(delete_contact(args, book))

        # Невідома команда
        else:
            print("Невідома команда. Спробуйте ще раз.")


# =========================
# ТОЧКА ВХОДУ
# =========================

if __name__ == "__main__":
    main()