from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import (User, Device)

from .validators import phone_validator
# from profiles.serializers import ProfileSerializer
# from segment.tracker import send_stats

from .exceptions import (
    UserNotFound, UserDeactivated, PhoneNotProvided,
    CountryPhoneCodeNotProvided, CountryCodeNotProvided,
    CountryNameNotProvided, CellPhoneExist, EmailExists,
    PasswordNotProvided, DeviceNotProvided,
    NameNotProvided, EmailNotProvided
)


class RegistrationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(max_length=64, read_only=True)
    signedup = serializers.BooleanField(read_only=True)
    device_uuid = serializers.CharField(max_length=255, write_only=True)
    platform_type = serializers.IntegerField(max_value=2, min_value=0, write_only=True)
    time_zone = serializers.CharField(max_length=250, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['token', 'email', 'device_uuid', 'platform_type', 'signedup']

    def create(self, validated_data):
        device = Device.objects.get_or_create_device(**validated_data)

        try:
            user_obj = User.objects.get(devices__device=device.device)
        except User.DoesNotExist:
            user_obj = User.objects.create_user(**validated_data)
            user_obj.devices.add(device)

        if user_obj.signed_up:
            user = user_obj
        else:
            user = authenticate(email=user_obj.email, password='jhewbnGSFHVDwdbv23e78Sdhjag')

        if user is None:
            raise UserNotFound
        if not user.is_active:
            raise UserDeactivated

        return {
            'email': user.email,
            'token': user.token,
            'signedup': user.signed_up
        }


class RegistrationDataSerializer(serializers.ModelSerializer):
    """For backend-update, but for client - as post."""
    token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    email = serializers.CharField(max_length=35, required=True)

    class Meta:
        model = User
        fields = ['token', 'password', 'email']

    def update(self, instance, validated_data):

        email = validated_data.get('email', None)
        if email is None:
            raise EmailNotProvided

        password = validated_data.get('password', None)
        if password is None:
            raise PasswordNotProvided

        obj = User.objects.filter(email=email).first()

        if obj is not None:
            raise EmailExists
        instance.signed_up = True
        instance.set_password(password)
        instance.email = email
        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(max_length=64, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    device_uuid = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'token', 'device_uuid'
        )

    def validate(self, data):
        password = data.get('password', None)
        email = data.get('email', None)
        device_uuid = data.get('device_uuid', None)

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise e('User not found!')

        if password is None:
            raise PasswordNotProvided

        if device_uuid is None:
            raise DeviceNotProvided

        user = authenticate(email=user_obj.email, password=password)

        if user is None:
            raise UserNotFound

        if not user.is_active:
            raise UserDeactivated

        try:
            device = Device.objects.get(device=device_uuid)
        except Device.DoesNotExist:
            device = Device.objects.create(device=device_uuid)

        try:
            User.objects.get(devices__device=device.device)
        except User.DoesNotExist:
            user.devices.add(device)

        if not user.mobile_device:
            user.mobile_device = True
            user.save()

        return {
            'cellphone': user.cellphone,
            'token': user.token,
        }


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # profile = ProfileSerializer(write_only=True)

    bio = serializers.CharField(source='profile.bio', read_only=True)
    imageURL = serializers.CharField(source='profile.imageURL', read_only=True)
    full_name = serializers.CharField(source='profile.full_name')

    class Meta:
        model = User
        fields = (
            'email', 'password', 'token', 'bio',
            'imageURL', 'full_name'
        )
        read_only_fields = ('token', )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password is not None:
            instance.set_password(password)

        # profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.signed_up = True
        instance.save()

        # for (key, value) in profile_data.items():
        #     setattr(instance.profile, key, value)
        # instance.profile.save()

        # send_stats.delay(3, user_id=instance.uuid, data={'name': instance.profile.full_name})

        return instance
