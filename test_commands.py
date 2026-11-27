import tempfile
import unittest
from pathlib import Path

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
from contacts import AddressBook
from notes_storage import load_notes, save_notes


class TestContactCommands(unittest.TestCase):
    def setUp(self):
        self.address_book = AddressBook()

    def test_contact_lifecycle_and_fields(self):
        self.assertEqual(add_contact(
            ["Olena", "0501234567"], self.address_book), "Contact added.")
        self.assertEqual(show_phones(
            ["Olena"], self.address_book), "0501234567")

        self.assertEqual(change_phone(
            ["Olena", "0679876543"], self.address_book), "Phone updated.")
        self.assertEqual(show_phones(
            ["Olena"], self.address_book), "0679876543")

        self.assertEqual(add_birthday(
            ["Olena", "15.05.1995"], self.address_book), "Birthday added.")
        self.assertEqual(show_birthday(
            ["Olena"], self.address_book), "15.05.1995")

        self.assertEqual(
            add_email(["Olena", "olena@example.com"], self.address_book), "Email added.")
        self.assertEqual(show_email(
            ["Olena"], self.address_book), "olena@example.com")

        self.assertEqual(add_address(
            ["Olena", "Khreshchatyk", "St", "10"], self.address_book), "Address added.")
        self.assertEqual(show_address(
            ["Olena"], self.address_book), "Khreshchatyk St 10")

        found = find_contact(["Olena"], self.address_book)
        self.assertIn("Olena", found)

        self.assertEqual(delete_contact(
            ["Olena"], self.address_book), "Contact deleted.")
        self.assertEqual(find_contact(
            ["Olena"], self.address_book), "Contact not found")

    def test_missing_arguments_and_unknown_contact(self):
        self.assertEqual(add_contact([], self.address_book),
                         "Enter the argument for the command")
        self.assertEqual(change_phone(
            ["Unknown", "0501112233"], self.address_book), "Contact not found")
        self.assertEqual(show_phones(
            ["Unknown"], self.address_book), "Contact not found")
        self.assertEqual(show_birthday(
            ["Unknown"], self.address_book), "Contact not found")
        self.assertEqual(show_email(
            ["Unknown"], self.address_book), "Contact not found")
        self.assertEqual(show_address(
            ["Unknown"], self.address_book), "Contact not found")


class TestNotesBookAndStorage(unittest.TestCase):
    def test_notes_operations_and_csv_persistence(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            notes_file = Path(tmp_dir) / "notes.csv"
            notes_book = load_notes(notes_file)

            n1 = notes_book.add_note(
                "Shopping", "Buy milk and bread", {"home", "food"})
            n2 = notes_book.add_note(
                "Work", "Finish report on project", {"work"})
            notes_book.add_note("Idea", "Draft new feature")

            self.assertEqual(n1.id, 1)
            self.assertEqual(n2.id, 2)
            self.assertTrue(notes_book.add_tag(1, "urgent"))
            self.assertEqual(len(notes_book.search_notes("report")), 1)
            self.assertEqual(len(notes_book.search_by_tag("work")), 1)
            self.assertTrue(notes_book.edit_note(3, title="New Idea"))

            sorted_notes = notes_book.sort_by_tags()
            self.assertEqual(len(sorted_notes), 3)

            save_notes(notes_book, notes_file)
            reloaded = load_notes(notes_file)

            self.assertEqual(len(reloaded.all_notes()), 3)
            self.assertEqual(reloaded.next_id, 4)
            self.assertEqual(reloaded.find_note(1).tags,
                             {"home", "food", "urgent"})

            self.assertTrue(reloaded.delete_note(2))
            self.assertFalse(reloaded.delete_note(999))
            deleted_count = reloaded.delete_all_notes()
            self.assertEqual(deleted_count, 2)
            self.assertEqual(len(reloaded.all_notes()), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
