import unittest
import os
from library import Library, BookNotFoundError

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.test_filename = 'test_library.json'
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        self.library = Library(self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_book(self):
        self.library.add_book("Финансист", "Теодор Драйзер", 1912)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[1].title, "Финансист")

    def test_remove_book(self):
        self.library.add_book("Стоик", "Теодор Драйзер", 1947)
        book_id = 1
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)
        with self.assertRaises(BookNotFoundError):
            self.library.remove_book(book_id) 

    def test_search_books(self):
        self.library.add_book("Оплот", "Теодор Драйзер", 1940)
        results = self.library.search_books("Оплот")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Оплот")

    def test_update_status(self):
        self.library.add_book("Финансист", "Теодор Драйзер", 1912)
        book_id = 1
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[book_id].status, "выдана")
        with self.assertRaises(BookNotFoundError):
            self.library.update_status(999, "выдана")

    def test_save_load_books(self):
        self.library.add_book("Стоик", "Теодор Драйзер", 1947)
        self.library.save_books()
        new_library = Library(self.test_filename)
        self.assertEqual(len(new_library.books), 1) 
        self.assertEqual(new_library.books[1].title, "Стоик") 

if __name__ == '__main__':
    unittest.main()