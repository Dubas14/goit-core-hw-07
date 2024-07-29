from datetime import datetime, timedelta

# Базовий клас для полів
class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

# Клас для телефонного номера
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Телефонний номер має складатися з 10 цифр.")
        super().__init__(value)

# Клас для дня народження, який перевіряє правильність формату та перетворює рядок на об'єкт datetime
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY.")

# Клас для запису контакту, який включає ім'я, телефони та д.р.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Метод для додавання телефону до контакту
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Метод для додавання дня народження до контакту
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

# Клас для адресної книги, який зберігає всі контакти
class AddressBook:
    def __init__(self):
        self.records = {}

    # Метод для додавання запису до адресної книги
    def add_record(self, record):
        self.records[record.name.value] = record

    # Метод для пошуку запису за ім'ям
    def find(self, name):
        return self.records.get(name, None)

    # Метод для отримання днів народження на найближчі 7 днів
    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.records.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if today <= bday <= today + timedelta(days=7):
                    upcoming_birthdays.append({"name": record.name.value, "birthday": bday.strftime("%d.%m.%Y")})
        return upcoming_birthdays

# Декоратор для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Невірний формат. Будь ласка, введіть ім'я та номер телефону."
    return inner

# Функція для розбору введення користувача
def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    cmd = cmd.lower()
    return cmd, args

# Функція для додавання контакту
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Контакт оновлено."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    if phone:
        record.add_phone(phone)
    return message

# Функція для зміни телефону контакту
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        for phone in record.phones:
            if phone.value == old_phone:
                record.phones.remove(phone)
                record.add_phone(new_phone)
                return "Контакт оновлено."
        raise KeyError
    else:
        raise KeyError

# Функція для показу телефону контакту
@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return ", ".join(phone.value for phone in record.phones)
    else:
        raise KeyError

# Функція для показу всіх контактів
@input_error
def show_all(args, book: AddressBook):
    if args:
        raise ValueError
    if book.records:
        return "\n".join([f"{record.name.value}: {', '.join(phone.value for phone in record.phones)}" for record in book.records.values()])
    else:
        return "Контакти не знайдено."

# Функція для додавання дня народження до контакту
@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "День народження додано."
    else:
        raise KeyError

# Функція для показу дня народження контакту
@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime('%d.%m.%Y')
    else:
        raise KeyError

# Функція для показу днів народження на найближчі 7 днів
@input_error
def birthdays(args, book: AddressBook):
    if args:
        raise ValueError
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{entry['name']}: {entry['birthday']}" for entry in upcoming_birthdays])
    else:
        return "Немає днів народження на найближчі 7 днів."

# Головна функція, яка реалізує логіку роботи бота
def main():
    book = AddressBook()
    print("Вітаю! Я ваш помічник-бот.")
    print("Введіть одну з команд: ")
    print("hello - отримати привітання ")
    print("add [ім'я] [номер телефону] - додати новий контакт ")
    print("change [ім'я] [старий номер телефону] [новий номер телефону] - змінити існуючий контакт ")
    print("phone [ім'я] - показати номер телефону для заданого контакту ")
    print("all - показати всі контакти")
    print("add-birthday [ім'я] [дата народження] - додати день народження для контакту ")
    print("show-birthday [ім'я] - показати день народження контакту ")
    print("birthdays - показати дні народження на найближчі 7 днів ")
    print("close або exit - завершити роботу бота")

    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break
        elif command == "hello":
            print("Чим можу допомогти?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Невірна команда. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
