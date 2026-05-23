import json
from pathlib import Path

DATA_PATH = Path("books.json")


def read_library():
    """Загружает записи из JSON-файла."""
    if not DATA_PATH.exists():
        return []

    try:
        with DATA_PATH.open("r", encoding="utf-8") as source:
            content = json.load(source)
            if isinstance(content, list):
                return content
            return []
    except json.JSONDecodeError:
        print("Файл с книгами повреждён. Будет открыт пустой список.")
        return []


def write_library(records):
    """Сохраняет список книг в JSON-файл."""
    with DATA_PATH.open("w", encoding="utf-8") as target:
        json.dump(records, target, ensure_ascii=False, indent=4)


def ask_mark():
    """Запрашивает оценку от 1 до 5."""
    while True:
        raw_value = input("Поставьте оценку книге от 1 до 5: ").strip()

        try:
            mark = int(raw_value)
        except ValueError:
            print("Нужно ввести число, например 4.")
            continue

        if 1 <= mark <= 5:
            return mark

        print("Оценка должна быть в диапазоне от 1 до 5.")


def already_exists(records, writer, book_name):
    """Проверяет, есть ли такая книга в журнале чтения."""
    normalized_writer = writer.strip().casefold()
    normalized_name = book_name.strip().casefold()

    for item in records:
        same_writer = item["author"].strip().casefold() == normalized_writer
        same_name = item["title"].strip().casefold() == normalized_name
        if same_writer and same_name:
            return True

    return False


def add_new_record():
    """Добавляет новую прочитанную книгу."""
    library = read_library()

    writer = input("Введите автора: ").strip()
    book_name = input("Введите название произведения: ").strip()

    if not writer or not book_name:
        print("Автор и название не могут быть пустыми.")
        return

    if already_exists(library, writer, book_name):
        print("Такая книга уже записана в журнал. Повтор не добавлен.")
        return

    mark = ask_mark()
    finish_date = input("Укажите дату прочтения, например 23.05.2026: ").strip()

    if not finish_date:
        print("Дата прочтения не заполнена. Запись отменена.")
        return

    new_item = {
        "author": writer,
        "title": book_name,
        "rating": mark,
        "read_date": finish_date,
    }

    library.append(new_item)
    write_library(library)
    print("Запись добавлена в читательский журнал.")


def show_records():
    """Показывает все сохранённые книги."""
    library = read_library()

    if not library:
        print("Пока нет ни одной сохранённой книги.")
        return

    print("\nВаш читательский журнал:")
    for position, item in enumerate(library, start=1):
        print(
            f"{position}. {item['author']} — {item['title']} | "
            f"оценка: {item['rating']} | дата: {item['read_date']}"
        )


def show_average_mark():
    """Показывает среднюю оценку по всем книгам."""
    library = read_library()

    if not library:
        print("Среднюю оценку пока считать не из чего.")
        return

    total = sum(item["rating"] for item in library)
    average = total / len(library)

    print(f"Средняя оценка по прочитанным книгам: {average:.2f}")


def show_writer_summary():
    """Показывает количество книг по каждому автору."""
    library = read_library()

    if not library:
        print("Статистика авторов пока пустая.")
        return

    summary = {}

    for item in library:
        writer = item["author"]
        summary[writer] = summary.get(writer, 0) + 1

    print("\nСтатистика по авторам:")
    for writer, amount in summary.items():
        print(f"{writer}: {amount} книг(и)")


def remove_record():
    """Удаляет книгу по номеру в списке."""
    library = read_library()

    if not library:
        print("Удалять нечего: список книг пуст.")
        return

    show_records()

    try:
        number = int(input("Введите номер книги для удаления: ").strip())
    except ValueError:
        print("Нужно ввести номер из списка.")
        return

    if number < 1 or number > len(library):
        print("Книги с таким номером нет.")
        return

    removed = library.pop(number - 1)
    write_library(library)

    print(f"Удалена запись: {removed['author']} — {removed['title']}.")


def print_actions():
    """Выводит главное меню."""
    print("\n=== Журнал прочитанных книг ===")
    print("1. Записать новую книгу")
    print("2. Вывести весь журнал")
    print("3. Рассчитать среднюю оценку")
    print("4. Показать сводку по авторам")
    print("5. Удалить запись о книге")
    print("6. Завершить работу")


def main():
    while True:
        print_actions()
        command = input("Введите номер действия: ").strip()

        if command == "1":
            add_new_record()
        elif command == "2":
            show_records()
        elif command == "3":
            show_average_mark()
        elif command == "4":
            show_writer_summary()
        elif command == "5":
            remove_record()
        elif command == "6":
            print("Программа завершена. Данные сохранены в books.json.")
            break
        else:
            print("Такого пункта меню нет. Выберите число от 1 до 6.")


if __name__ == "__main__":
    main()