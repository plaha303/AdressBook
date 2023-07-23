from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)


class Name(Field):
    def validate(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("The name must be a non-empty string.")


class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number. Please enter a 10-digit number.")


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.format = "%d.%m.%Y"

    def validate(self, value):
        try:
            datetime.strptime(value, self.format)
        except ValueError:
            raise ValueError("Incorrect birthday format. Please use the format DD.MM.YYYY")

    def get_date(self):
        return datetime.strptime(self.value, self.format)


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def del_phone(self, phone: Phone):
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return f"phone {phone} removed from contact {self.name}"
        return f"{phone} not present in phones of contact {self.name}"

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
            return f"{old_phone} not present in phones of contact {self.name}"

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = self.birthday.get_date().replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_remaining = (next_birthday - today).days
            return days_remaining
        return None

    def __str__(self):
        phones_str = ", ".join(str(p) for p in self.phones)
        return f"Name: {self.name}, Phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def delete_record(self, name):
        del self.data[name]

    def edit_record(self, name, new_record):
        self.data[name] = new_record

    def search_records(self, **kwargs):
        results = []
        for record in self.data.values():
            match = True
            for key, value in kwargs.items():
                if key == "name":
                    if str(record.name).lower() != value.lower():
                        match = False
                        break
                elif key == "phone":
                    phone_match = False
                    for phone in record.phones:
                        if str(phone).lower() == value.lower():
                            phone_match = True
                            break
                    if not phone_match:
                        match = False
                        break
            if match:
                results.append(record)
        return results

    def iterator(self, batch_size, page_number):
        data_values = list(self.data.values())
        start_idx = page_number * batch_size
        end_idx = min((page_number + 1) * batch_size, len(data_values))
        return data_values[start_idx:end_idx]

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
