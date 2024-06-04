from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from phone_field import PhoneField

from . import core as core_models


class CoreUserData(core_models.CoreModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    secondary_email = models.EmailField(max_length=255, blank=True, null=True)
    home_phone = PhoneField(blank=True, null=True)
    mobile_phone = PhoneField(blank=True, null=True)
    work_phone = PhoneField(blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True, default="")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True, default="")
    city = models.CharField(max_length=255, blank=True, null=True, default="")
    state = models.CharField(max_length=255, blank=True, null=True, default="")
    timezone = models.CharField(max_length=255, default=timezone.get_default_timezone_name())


class CoreUserManager(models.Manager):
    def get_or_create_system_user(self):
        try:
            system_user = CoreUser.objects.get(pk='45407f07-21e9-42ba-8c39-03b57767fe76')
        except CoreUser.DoesNotExist:
            system_user = CoreUser(
                id='45407f07-21e9-42ba-8c39-03b57767fe76',
                created_by_id='45407f07-21e9-42ba-8c39-03b57767fe76',
            )
            system_user.save()
            system_user_data = CoreUserData(
                id='02e94188-5b8e-494a-922c-bc6ed2ffcfc4',
                created_by_id='45407f07-21e9-42ba-8c39-03b57767fe76',
                first_name='SYSTEM',
                last_name='USER',
                address_line_1='',
                address_line_2='',
                city='',
                state='',
                postal_code=0
            )
            system_user_data.save()
            system_user.core_user_data = system_user_data
            system_user.save()

        return system_user


class CoreUser(core_models.CoreModel):
    objects = CoreUserManager()

    core_user_data = models.OneToOneField(CoreUserData, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
