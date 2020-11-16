from random import randint


"""
Password generator
"""


class Creditentials(object):
    cap_letters = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
        'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
        'V', 'W', 'X', 'Y', 'Z'
    ]
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z'
    ]

    def random_letter(self):
        result = ''
        where = randint(0, 1)
        number = randint(0, 25)
        if where == 1:
            result = self.cap_letters[number]
        else:
            result = self.letters[number]
        return str(result)

    def random_number(self):
        return str(randint(1, 9))

    def generate_random_password(self):
        result = ''
        i = 0
        while i <= 14:
            if i != 3 or i != 7 or i != 11:
                where = randint(0, 1)
                if where == 0:
                    result += self.random_letter()
                else:
                    result += self.random_number()
            else:
                result += '-'
            i += 1
        return result

    def generate_access_code(self):
        return int(randint(1000, 9999))

    def generate_creditentials(self, phone, country_code):
        name = str(phone)
        i = 0
        while i <= 7:
            where = randint(0, 1)
            if where == 0:
                name += self.random_letter()
            else:
                name += self.random_number()
            i += 1
        name = name + country_code
        email = name + "@gmail.com"
        return [name, email]

    def generate_creditentials_from_uuid(self, device_uuid, platform):
        raw = str(device_uuid)
        name = self.generate_randon_name_from_device(device_uuid, platform, len(raw))
        email = name + "@gmail.com"
        phone = self.generate_new_phone_from_name(name, False)
        country_name = 'Unknown'
        country_code = 'Un'
        code_save = '+0'
        valid_country = False
        return [name, email, phone, country_name, country_code, code_save, valid_country]

    def generate_randon_name_from_device(self, device_uuid, platform, length):
        if platform == 0:
            pl = 'iOS'
        elif platform == 1:
            pl = 'Android'
        else:
            pl = 'Web'

        name = pl + "_"

        i = 0
        if length > 0:
            input_list = list(device_uuid)
            while i <= len(input_list):
                name += input_list[randint(0, len(input_list) - 1)]
                i += 1
        else:
            while i <= 25:
                where = randint(0, 1)
                if where == 0:
                    name += self.random_letter()
                else:
                    name += self.random_number()
                i += 1

        return name

    def generate_username_from_name(self, fullname, platform):
        if platform == 0:
            pl = 'iOS'
        elif platform == 1:
            pl = 'Android'
        else:
            pl = 'Web'

        name = pl + "_"
        i = 0
        input_list = list(fullname)
        while i <= len(input_list) - 1:
            if input_list[i] == " ":
                name += "_"
            else:
                where = randint(0, 1)
                if where == 0:
                    name += input_list[i]
                else:
                    name += input_list[i].upper()
            i += 1
        name += str(randint(100, 999))

        return name

    def generate_new_phone_from_name(self, name, generate):
        if len(name) >= 24:
            phone = name[0:23]
        else:
            phone = name

        if generate:
            phone = ""
            input_list = list(phone)
            i = 0
            while i <= len(input_list):
                phone += input_list[randint(0, len(input_list) - 1)]

        return phone


Creditentials = Creditentials()
