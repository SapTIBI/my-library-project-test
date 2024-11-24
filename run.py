import json
import os
from typing import Dict, Any, List


class BookNotFoundError(Exception):
    """Ошибка, когда книга с указанным ID не найдена."""
    pass

class Book:
    def __init__(self, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = None 
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

class Library:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self) -> Dict[int, Book]:
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            books = {item['id']: self.dict_to_book(item) for item in data}
            return books

    def dict_to_book(self, data: Dict[str, Any]) -> Book:
        book = Book(data['title'], data['author'], data['year'], data['status'])
        book.id = data['id']
        return book

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books.values()], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        new_book = Book(title, author, year)
        new_book.id = self.get_new_id()
        self.books[new_book.id] = new_book
        self.save_books()

    def get_new_id(self) -> int:
        return max(self.books.keys()) + 1 if self.books else 1

    def remove_book(self, book_id: int):
        if book_id in self.books:
            del self.books[book_id]
            self.save_books()
        else:
            raise BookNotFoundError("Книга с данным ID не найдена.")

    def search_books(self, query: str) -> List[Book]:
        query = query.lower()
        results = [book for book in self.books.values() if query in book.title.lower() or query in book.author.lower() or query == str(book.year)]
        return results

    def display_books(self):
        for book in self.books.values():
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

    def update_status(self, book_id: int, status: str):
        if book_id in self.books:
            self.books[book_id].status = status
            self.save_books()
        else:
            raise BookNotFoundError("Книга с данным ID не найдена.")

def main():
    library = Library('library.json')
    command_list_msg = """
    Доступные команды:
    1. Добавить книгу
    2. Удалить книгу
    3. Поиск книги
    4. Отобразить все книги
    5. Изменить статус книги
    6. Выход
    """
    while True:
        print(command_list_msg)
        choice = input("Выберите действие: ")
        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            try:
                year = int(input("Введите год издания: "))
                library.add_book(title, author, year)
                print("Книга добавлена.")
            except ValueError:
                print('Год издания должен представлять из себя целое число, повторите попытку!')
            except Exception as e:
                print('Что-то пошло не так, повторите попытку!')
        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            try:
                library.remove_book(book_id)
                print("Книга удалена.")
            except ValueError as e:
                print('ID книги должно представлять из себя целое число, повторите попытку!')
            except Exception as e:
                print('Что-то пошло не так, повторите попытку!')
        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            results = library.search_books(query)
            if results:
                for book in results:
                    print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")
            else:
                print("Книги не найдены.")
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            try:
                book_id = int(input("Введите ID книги для изменения статуса: "))
            except ValueError:
                print('Введен некорректный ID')
                continue
            except Exception as e:
                print('Что-то пошло не так, повторите попытку!')
                continue
            status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            if status.lower().strip() not in ['в наличии', 'выдана']:
                print('Введен некорректный статус для книги')
                continue
            try:
                library.update_status(book_id, status)
                print("Статус книги обновлен.")
            except BookNotFoundError as e:
                print('Книга с таким ID не была найдена!')
            except Exception as e:
                print('Что-то пошло не так, повторите попытку!')
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Недопустимый выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()