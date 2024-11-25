
from library import Library, BookNotFoundError


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