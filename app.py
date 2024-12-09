from collections import UserDict
import datetime as dt
from datetime import datetime as dtdt
import pickle
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
class Name(Field):
    pass
class Phone(Field):
    def check(self):
        lenght = self
        if len(lenght) == 10:
            return self
        else: 
            raise Exception("Wrong number format. Should be 10 digits.")
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = dtdt.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    def add_phone(self, phone):
        self.phones.append(str(Phone.check(phone)))
    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
    def edit_phone(self, old, new):
        if old in self.phones:
            self.phones.remove(old)
        self.phones.append(str(Phone.check(new)))
    def find_phone(self, phone):
        for phone in self.phones:
            if phone in self.phones:
                return phone
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {', '.join(ph for ph in self.phones)}"
class AddressBook(UserDict):
    def add_record(self, kontact):
        self.data[kontact.name.value]=kontact
    def find(self, name) -> Record:
        return self.data.get(name)
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    def get_upcoming_birthdays(self):
        tdate = dtdt.today().date()
        birthdays = []
        for user in self.data:
            userr = self.find(user) 
            nam = userr.name.value
            try:
                bir = userr.birthday.value
                bir = dtdt.strftime(bir, "%Y,%m,%d")
                bir = str(tdate.year)+bir[4:]
                bir = dtdt.strptime(bir, "%Y,%m,%d").date()
                week_day = bir.isoweekday()
                days_between = (bir - tdate).days
                if 0<=days_between<7:
                    if week_day<6:
                        birthdays.append({'name':nam, 'birthday':bir.strftime("%Y,%m,%d")})
                    else:
                        if (bir+dt.timedelta(days=1)).weekday()==0:
                            birthdays.append({'name':nam, 'birthday': (bir+dt.timedelta(days=1)).strftime("%Y,%m,%d")})
                        elif (bir+dt.timedelta(days=2)).weekday()==0:
                            birthdays.append({'name':nam, 'birthday': (bir+dt.timedelta(days=2)).strftime("%Y,%m,%d")})
            except Exception:
                continue
        return birthdays           
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Key not found"
        except IndexError:
            return "Index not found"
    return inner
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
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
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone,  *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        return "Contact not found"
    else:
        record.remove_phone(old_phone)
        record.add_phone(new_phone)
    return message
@input_error
def phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    else:
        return record
@input_error
def all(book: AddressBook):
    string = ""
    for rec in book:
        record = book.find(rec)
        string_phones = ', '.join(record.phones)
        result = f"Contact name: {record.name.value}, phones: {string_phones}"
        string += result + "\n"
    return string
@input_error
def add_birthday(args, book:AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    else:
        record.add_birthday(birthday)
    return "Birthday added."
@input_error
def show_birthday(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    else:
        return record.birthday
@input_error
def birthdays(book:AddressBook):
    result = book.get_upcoming_birthdays()
    return result
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(phone(args, book))
        elif command == "all":
            print(all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        save_data(book)
if __name__ == "__main__":
    main()
