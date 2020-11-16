from rest_framework.exceptions import APIException


class PhoneValidationError(APIException):
    status_code = 400
    default_detail = 'Phone is invalid. Please, try again.'
    default_code = 'phone_validation_error'


class CellPhoneExist(APIException):
    status_code = 400
    default_detail = 'This phone number is already exists.'
    default_code = 'call_phone_exists'


class EmailExist(APIException):
    status_code = 400
    default_detail = 'This email is already exists.'
    default_code = 'email_exists'


class EmailNotProvided(APIException):
    status_code = 400
    default_detail = 'You lost email. It is required field.'
    default_code = 'email_not_provided'


class PasswordNotProvided(APIException):
    status_code = 400
    default_detail = 'Password is required.'
    default_code = 'password_not_provided'


class PhoneNotProvided(APIException):
    status_code = 400
    default_detail = 'Please, enter your phone.'
    default_code = 'phone_not_provided'


class CountryPhoneCodeNotProvided(APIException):
    status_code = 400
    default_detail = 'You lost your country phone code.'
    default_code = 'country_phone_code_not_provided'


class CountryCodeNotProvided(APIException):
    status_code = 400
    default_detail = 'You lost your country code.'
    default_code = 'country_code_not_provided'


class CountryNameNotProvided(APIException):
    status_code = 400
    default_detail = 'You lost your country.'
    default_code = 'country_not_provided'


class DeviceNotProvided(APIException):
    status_code = 400
    default_detail = 'You lost your device type.'
    default_code = 'device_not_provided'


class NameNotProvided(APIException):
    status_code = 400
    default_detail = 'You lost your name.'
    default_code = 'name_not_provided'


class EmailExists(APIException):
    status_code = 400
    default_detail = 'User with this email is already exists.'
    default_code = 'email_exists'


class UserDeactivated(APIException):
    status_code = 403
    default_detail = 'Your account deactivated. Activate it, please.'
    default_code = 'user_deactivated'


class UserNotFound(APIException):
    status_code = 404
    default_detail = 'User not found, try again.'
    default_code = 'user_not_found'
