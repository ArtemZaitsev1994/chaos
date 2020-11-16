import string


class DelitSymbols:

    def __init__(self, keep=string.digits):
        self.comp = dict((ord(c), c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)


DD = DelitSymbols()


def phone_validator(phone, country_phone_code):
    # check if the phone is with plus. e.g. user added it with country code
    if phone[0] == "+":

        clean_number = clean_phone(phone[1:])

        # check if the selected country phone code is equal to inputed country phone code
        code_length = len(country_phone_code)

        add_plus_number = "+" + clean_number

        if add_plus_number[0:code_length] == country_phone_code:
            return {"phone": str(add_plus_number[code_length:]), "code": country_phone_code}  # actual phone number
        else:
            return {"phone": add_plus_number, "code": None}

    else:
        clean_number = clean_phone(phone)
        return {"phone": clean_number, "code": str(country_phone_code)}


def clean_phone(phone):
    # leave only digits
    return str(phone.translate(DD))
