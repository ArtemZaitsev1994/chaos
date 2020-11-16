from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .utils import Creditentials
from .validators import phone_validator
# from .exceptions import (
#     CellPhoneExist, EmailExist,
#     EmailNotProvided, PasswordNotProvided,
#     PhoneNotProvided
# )
from core.utils import get_today


class UserManager(BaseUserManager):

    def get_by_uuid(self, uuid):
        return self.filter(uuid=uuid).first()

    def create_user(self, device_uuid, platform_type, time_zone=None, **kwargs):
        """Create and return a `User` with an email and password."""
        if not device_uuid:
            raise ValueError('Users must have a valid device_uuid')

        if not platform_type:
            platform_type = 0

        generate = Creditentials.generate_creditentials_from_uuid(device_uuid, platform_type)

        password = 'jhewbnGSFHVDwdbv23e78Sdhjag'
        conformation_code = Creditentials.generate_access_code()

        user = self.model(
            email=self.normalize_email(generate[1]), cellphone=generate[2],
            country_name=generate[3], country_code=generate[4],
            country_phone_code=generate[5], phone_verification_code=conformation_code,
            phone_code_valid=generate[6], is_active=True, time_zone='time_zone'
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def check_the_phone_exist(self, phone, code):
        phone_valid = phone_validator(phone, "+" + code)
        try:
            self.get(cellphone=phone_valid['phone'], country_phone_code=phone_valid['code'])
            raise CellPhoneExist
        except ObjectDoesNotExist:
            return phone_valid

    def check_the_email_exist(self, email):
        try:
            self.get(email=email)
            raise EmailExist
        except ObjectDoesNotExist:
            return email


class DeviceManager(models.Manager):

    def get_or_create_device(self, device_uuid, platform_type, **kwargs):
        if not device_uuid:
            raise ValueError('Users must have a valid device_uuid')

        if not platform_type:
            platform_type = 0
        device_obj = self.filter(device=device_uuid, device_type=int(platform_type)).first()
        if device_obj is None:
            device_obj = self.model(device=device_uuid, device_type=int(platform_type))
            device_obj.save()
        return device_obj


class SmsLogManager(models.Manager):

    def check_to_send(self, user):
        sms_objs_count = self.filter(user_uuid=user.uuid, created_at__lte=get_today()).count()
        if sms_objs_count > 10:
            return False
        else:
            return True
