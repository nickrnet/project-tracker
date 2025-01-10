from django.contrib.auth.models import User as DjangoUser

from core.management.commands.modules.test_organization_data_01 import test_organization_01
from core.management.commands.modules.test_organization_data_02 import test_organization_02
from core.models import organization as core_organization_models
from core.models import user as core_user_models
from project.models import project as project_models


test_user_03 = {
    'first_name': 'Alice',
    'middle_name': '',
    'last_name': 'TestUser03',
    'email': 'test_user_03@project-tracker.dev',
    'secondary_email': '',
    'home_phone': '123-456-7890',
    'mobile_phone': '123-456-7890',
    'work_phone': '123-456-7890',
    'address_line_1': '123 Main St',
    'address_line_2': '',
    'postal_code': '12345',
    'city': 'Anytown',
    'state': 'NY',
    'postal_code': '12345',
    'country': 'USA',
    'timezone': 'America/Chicago',
    'password': 'password123'
    }


def initialize_test_user_03():
    api_user = core_user_models.CoreUser.objects.get_or_create_api_user()

    django_user = DjangoUser.objects.create_user(
        username=test_user_03.get('email'),
        email=test_user_03.get('email'),
        password=test_user_03.get('password')
        )

    core_user_data = core_user_models.CoreUserData(
        created_by_id=api_user.id,
        first_name=test_user_03.get('first_name', ''),
        middle_name=test_user_03.get('middle_name', ''),
        last_name=test_user_03.get('last_name', ''),
        email=test_user_03.get('email'),
        secondary_email=test_user_03.get('secondary_email', ''),
        home_phone=test_user_03.get('home_phone', ''),
        mobile_phone=test_user_03.get('mobile_phone', ''),
        work_phone=test_user_03.get('work_phone', ''),
        address_line_1=test_user_03.get('address_line_1', ''),
        address_line_2=test_user_03.get('address_line_2', ''),
        city=test_user_03.get('city', ''),
        state=test_user_03.get('state', ''),
        postal_code=test_user_03.get('postal_code', ''),
        country=test_user_03.get('country', ''),
        timezone=test_user_03.get('timezone', ''),
        )
    core_user_data.save()

    new_user = core_user_models.CoreUser(
        created_by_id=api_user.id,
        current=core_user_data,
        user=django_user
        )
    new_user.save()

    test_organization_01_instance = core_organization_models.Organization.objects.get(
        current__name=test_organization_01.get('name'))
    test_organization_02_instance = core_organization_models.Organization.objects.get(
        current__name=test_organization_02.get('name'))
    test_organization_01_instance.members.add(new_user)
    test_organization_01_instance.save()
    test_organization_02_instance.members.add(new_user)
    test_organization_02_instance.save()

    test_project_01_instance = project_models.Project.objects.get(current__name='Test Project 01')
    test_project_02_instance = project_models.Project.objects.get(current__name='Test Project 02')
    test_project_01_instance.users.add(new_user)
    test_project_01_instance.save()
    test_project_02_instance.users.add(new_user)
    test_project_02_instance.save()
