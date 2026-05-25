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
        print("Не удалось прочитать books.json. Открыт пустой журнал.")
        return []


def write_library(records):
    """Сохраняет список книг в JSON-файл."""
    with DATA_PATH.open("w", encoding="utf-8") as target:
        json.dump(records, target, ensure_ascii=False, indent=4)


def ask_mark():
    """Запрашивает оценку от 1 до 5."""
    while True:
        raw_value = input("Оцените книгу по шкале от 1 до 5: ").strip()

        try:
            mark = int(raw_value)
        except ValueError:
            print("Введите именно число. Например: 4.")
            continue

        if 1 <= mark <= 5:
            return mark

        print("Оценка должна быть целым числом от 1 до 5.")


# Проверка дубликатов нужна, чтобы пользователь не добавлял одну и ту же книгу повторно.
# Дубликатом считается совпадение автора и названия книги.
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

    writer = input("Автор книги: ").strip()
    book_name = input("Название книги: ").strip()

    if not writer or not book_name:
        print("Запись не создана: автор и название обязательны.")
        return

    if already_exists(library, writer, book_name):
        print("Такая книга уже есть в журнале. Дубликат не сохранён.")
        return

    mark = ask_mark()
    finish_date = input("Дата прочтения, например 23.05.2026: ").strip()

    if not finish_date:
        print("Запись отменена: дата прочтения не указана.")
        return

    new_item = {
        "author": writer,
        "title": book_name,
        "rating": mark,
        "read_date": finish_date,
    }

    library.append(new_item)
    write_library(library)

    print("Книга успешно добавлена в журнал.")


def show_records():
    """Показывает все сохранённые книги."""
    library = read_library()

    if not library:
        print("Журнал пока пуст. Добавьте первую книгу через пункт 1.")
        return

    print("\n=== Список прочитанных книг ===")
    for position, item in enumerate(library, start=1):
        print(
            f"{position}. {item['author']} — {item['title']} | "
            f"оценка: {item['rating']} | прочитано: {item['read_date']}"
        )


def show_average_mark():
    """Показывает среднюю оценку по всем книгам."""
    library = read_library()

    if not library:
        print("Нет данных для расчёта средней оценки.")
        return

    total = sum(item["rating"] for item in library)
    average = total / len(library)

    print(f"Средняя оценка книг в журнале: {average:.2f}")


def show_writer_summary():
    """Показывает количество книг по каждому автору."""
    library = read_library()

    if not library:
        print("Сводка по авторам пока недоступна: журнал пуст.")
        return

    summary = {}

    for item in library:
        writer = item["author"]
        summary[writer] = summary.get(writer, 0) + 1

    print("\nСводка по авторам:")
    for writer, amount in summary.items():
        print(f"{writer}: {amount} записей")


def remove_record():
    """Удаляет книгу по номеру в списке."""
    library = read_library()

    if not library:
        print("Удаление невозможно: в журнале пока нет книг.")
        return

    show_records()

    try:
        number = int(input("Укажите номер записи для удаления: ").strip())
    except ValueError:
        print("Нужно ввести номер записи, например 1.")
        return

    if number < 1 or number > len(library):
        print("Записи с таким номером нет. Удаление отменено.")
        return

    removed = library.pop(number - 1)
    write_library(library)

    print(f"Удалена запись: {removed['author']} — {removed['title']}.")


def print_actions():
    """Выводит главное меню."""
    print("\n=== Электронный журнал чтения ===")
    print("1. Добавить прочитанную книгу")
    print("2. Показать список книг")
    print("3. Посчитать среднюю оценку")
    print("4. Показать сводку по авторам")
    print("5. Удалить книгу из журнала")
    print("6. Выйти")


def main():
    while True:
        print_actions()
        command = input("Выберите команду: ").strip()

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
            print("Работа завершена. Изменения сохранены в books.json.")
            break
        else:
            print("Команда не распознана. Введите число от 1 до 6.")


if __name__ == "__main__":
    main()