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
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, default="")
    postal_code = models.CharField(max_length=255, blank=True, null=True, default="")
    city = models.CharField(max_length=255, blank=True, null=True, default="")
    state = models.CharField(max_length=255, blank=True, null=True, default="")
    country = models.CharField(max_length=255, blank=True, null=True, default="")
    timezone = models.CharField(max_length=255, default=timezone.get_default_timezone_name())


class CoreUserActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class CoreUserManager(models.Manager):
    def get_or_create_api_user(self):
        try:
            api_user = CoreUser.objects.get(pk='75af4764-0f94-49f2-a6dc-3dbfe1b577f9')
        except CoreUser.DoesNotExist:
            api_user = CoreUser(
                id='75af4764-0f94-49f2-a6dc-3dbfe1b577f9',
                created_by_id='75af4764-0f94-49f2-a6dc-3dbfe1b577f9',
            )
            api_user.save()
            api_user_data = CoreUserData(
                id='373f414f-9692-4e5c-92f2-5781dbad5c04',
                created_by_id='75af4764-0f94-49f2-a6dc-3dbfe1b577f9',
                first_name='API',
                last_name='USER',
                address_line_1='',
                address_line_2='',
                city='',
                state='',
                country='',
                postal_code=0,
            )
            api_user_data.save()
            api_user.core_user_data = api_user_data
            api_user.save()

        return api_user

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
                country='',
                postal_code=0,
            )
            system_user_data.save()
            system_user.core_user_data = system_user_data
            system_user.save()

        return system_user

    def create_core_user_from_web(self, request_data):
        api_user = CoreUser.objects.get_or_create_api_user()

        django_user = User.objects.create_user(
            username=request_data.get('email'),
            email=request_data.get('email'),
            password=request_data.get('password')
        )

        core_user_data = CoreUserData(
            created_by_id=api_user.id,
            first_name=request_data.get('first_name', ''),
            last_name=request_data.get('last_name', ''),
            email=request_data.get('email'),
            secondary_email=request_data.get('secondary_email', ''),
            home_phone=request_data.get('home_phone', ''),
            mobile_phone=request_data.get('mobile_phone', ''),
            work_phone=request_data.get('work_phone', ''),
            address_line_1=request_data.get('address_line_1', ''),
            address_line_2=request_data.get('address_line_2', ''),
            postal_code=request_data.get('postal_code', ''),
            city=request_data.get('city', ''),
            state=request_data.get('state', ''),
            country=request_data.get('country', ''),
            timezone=request_data.get('timezone', ''),
        )
        core_user_data.save()

        new_core_user = CoreUser(
            created_by_id=api_user.id,
            core_user_data=core_user_data,
            user=django_user
        )
        new_core_user.save()

        return new_core_user


class CoreUser(core_models.CoreModel):
    class Meta:
        ordering = ['core_user_data__last_name', 'core_user_data__email']

    active_objects = CoreUserActiveManager()
    objects = CoreUserManager()

    core_user_data = models.OneToOneField(CoreUserData, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def deactivate_login(self):
        self.user.is_active = False
        self.user.save()
