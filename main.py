from metods import AddressBook, Name, Phone, Record

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
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


def del_phone():
    name = Name(input("Enter the name: "))
    phone = Phone(input("Enter the phone number: "))
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.del_phone(phone)
    return f"No contact {name} in address book"

@input_error
def change_phone():
    name = Name(input("Enter the name: "))
    old_phone = Phone(input("Enter the old phone number: "))
    new_phone = Phone(input("Enter the new phone number: "))
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.edit_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


# @input_error
# def get_phone():
#     name = input("Enter the name: ")
#     return CONTACTS[name]


@input_error
def show_all():
    return address_book


def helper():
    commands = {
        hello: "hello -> displays a welcome message.",
        add_contact: "add -> adds a new contact.",
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
