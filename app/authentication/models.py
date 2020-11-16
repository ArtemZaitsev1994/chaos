import jwt
import uuid
from json import JSONEncoder

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db import models
from core.models import TimestampedModel

from .managers import (UserManager, DeviceManager, SmsLogManager)


# Fixing UUID encoding
JSONEncoder_olddefault = JSONEncoder.default


def JSONEncoder_newdefault(self, o):
    if isinstance(o, uuid.UUID):
        return str(o)
    return JSONEncoder_olddefault(self, o)


JSONEncoder.default = JSONEncoder_newdefault


class SMSLog(TimestampedModel):
    user_uuid = models.UUIDField(primary_key=False, editable=False, blank=True, null=True)

    objects = SmsLogManager()


class Device(TimestampedModel):

    TYPE = (
        (0, 'iOS'),
        (1, 'Android'),
        (2, 'WEB')
    )

    device = models.CharField(max_length=250, default="")
    device_type = models.PositiveSmallIntegerField(default=0, choices=TYPE)

    objects = DeviceManager()


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):

    email = models.EmailField(db_index=True, unique=True)
    time_zone = models.CharField(max_length=100, default="UTC")

    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    country_name = models.CharField(max_length=30, default="Russia")
    country_code = models.CharField(max_length=10, default="Ru")
    country_phone_code = models.CharField(max_length=10, default="+7")
    cellphone = models.CharField(max_length=25, blank=True, null=True, unique=True)
    phone_verification_code = models.SmallIntegerField(default=0, null=True)
    phone_code_valid = models.BooleanField(default=False)
    use_country_code = models.BooleanField(default=True)

    devices = models.ManyToManyField(Device, blank=True, related_name="registered_user_devices")
    mobile_device = models.BooleanField(default=True)

    signed_up = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.email

    def get_name(self):
        return self.profile.full_name

    def get_short_name(self):
        return self.username

    def get_country(self):
        return self.country_code

    def get_country_name(self):
        return self.country_name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=9999)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')
