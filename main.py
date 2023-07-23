from metods import AddressBook, Name, Phone, Record, Birthday

address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input. Please enter name and phone number separated by a space."
        except IndexError:
            return "Invalid input. Please enter a command."
        except TypeError:
            return func()
    return wrapper


@input_error
def hello():
    return "How can I help you?"


@input_error
def add_contact():
    name = Name(input("Enter the name: "))
    phone = Phone(input("Enter the phone number: "))
    birthday = Birthday(input("Enter birthday in format 'DD.MM.YYYY'"))
    rec: Record = address_book.get(str(name))
    if rec:
        rec.add_phone(phone)
        rec.birthday = birthday
        return f"Phone number {phone} added for contact {name}. Birthday has also been updated."
    rec = Record(name, phone, birthday)
    address_book.add_record(rec)
    return f"Contact {name} successfully added."


def del_phone():
    name = Name(input("Enter the name: "))
    phone = Phone(input("Enter the phone number: "))
    rec: Record = address_book.get(str(name))
    if rec:
        rec.del_phone(phone)
        return f"The phone number {phone} has been removed from the contact {name}."
    return f"No contact {name} in address book"


@input_error
def change_phone():
    name = Name(input("Enter the name: "))
    old_phone = Phone(input("Enter the old phone number: "))
    new_phone = Phone(input("Enter the new phone number: "))
    rec: Record = address_book.get(str(name))
    if rec:
        rec.edit_phone(old_phone, new_phone)
        return f"The old phone number {old_phone} has been updated to {new_phone} for contact {name}."
    return f"No contact {name} in address book"


@input_error
def add_birthday():
    name = Name(input("Enter the name: "))
    birthday = Birthday(input("Enter birthday in format 'DD.MM.YYYY': "))
    rec: Record = address_book.get(str(name))
    if rec:
        rec.birthday = birthday
        return f"Birthday updated for contact {name}."
    return f"No contact {name} in address book"


@input_error
def days_to_birthday():
    name = Name(input("Enter the name: "))
    rec: Record = address_book.get(str(name))
    if rec and rec.birthday:
        days_left = rec.days_to_birthday()
        if days_left is not None:
            return f"Contact {name} birthday is {days_left} days away."
        return f"Contact {name} birthday is today!"
    return f"The contact {name} is not found in the address book or the birthday is not specified."


@input_error
def edit_birthday():
    name = Name(input("Enter the name: "))
    rec: Record = address_book.get(str(name))
    if rec:
        new_birthday = Birthday(input("Enter a new birthday (in DD.MM.YYYY format): "))
        rec.birthday = new_birthday
        return f"Birthday updated for contact {name}."
    return f"No contact {name} in address book"


@input_error
def show_all():
    page_number = 1
    batch_size = 5
    while True:
        records_batch = list(address_book.iterator(batch_size, page_number))
        if not records_batch:
            print("No more contacts to display.")
            break

        for record in records_batch:
            birthday_info = f", Birthday: {record.birthday.value}" if record.birthday else ""
            print(f"Name: {record.name}, Phones: {', '.join(str(phone) for phone in record.phones)}{birthday_info}")

        print("\nPage:", page_number)
        print("Press Enter to see the next page or type 'exit' to return to the main menu.")
        user_input = input()

        if user_input.lower() == 'exit':
            break
        else:
            page_number += 1


def helper():
    commands = {
        hello: "hello -> displays a welcome message.",
        add_contact: "add -> adds a new contact.",
        add_birthday: "birthday -> adds birthday to contact",
        edit_birthday: "edit bd -> changes the existing birthday value of a contact",
        days_to_birthday: "days -> shows how many days are left until the birthday",
        change_phone: "change -> changes the phone number of an existing contact.",
        del_phone: "del -> delete number from contact.",
        # get_phone: "phone -> displays the phone number of a contact.",
        show_all: "show all -> displays all contacts and their phone numbers.",
        helper: "help -> displays the list of available commands.",
        exit: "exit, close, good bye -> exits the program."
    }
    help_text = "Available commands:\n"
    for command, description in commands.items():
        help_text += f"{description}\n"
    return help_text


def main():
    print("Welcome!")
    commands = {
        "hello": hello,
        "add": add_contact,
        "birthday": add_birthday,
        "edit bd": edit_birthday,
        "days": days_to_birthday,
        "change": change_phone,
        "del": del_phone,
        # "phone": get_phone,
        "show all": show_all,
        "help": helper,
        "exit": exit,
        "good bye": exit,
        "close": exit
    }

    while True:
        command = input("Enter a command: ").lower()

        if command in commands:
            if command in ["exit", "good bye", "close"]:
                print("Good bye!")
                break
            elif command == "help":
                print(commands[command]())
            else:
                func = commands[command]
                print(func())
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
