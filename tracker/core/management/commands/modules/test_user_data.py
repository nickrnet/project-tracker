from django.contrib.auth.models import User as DjangoUser

from core.models import user as core_user_models


test_user_01 = {
    'first_name': 'John',
    'middle_name': 'TestUser01',
    'last_name': 'Doe',
    'email': 'test_user_01@project-tracker.dev',
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
    'timezone': 'America/New_York',
    'password': 'password123'
}


def initialize_test_user():
    api_user = core_user_models.CoreUser.objects.get_or_create_api_user()

    django_user = DjangoUser.objects.create_user(
        username=test_user_01.get('email'),
        email=test_user_01.get('email'),
        password=test_user_01.get('password')
    )

    core_user_data = core_user_models.CoreUserData(
        created_by_id=api_user.id,
        first_name=test_user_01.get('first_name', ''),
        middle_name=test_user_01.get('middle_name', ''),
        last_name=test_user_01.get('last_name', ''),
        email=test_user_01.get('email'),
        secondary_email=test_user_01.get('secondary_email', ''),
        home_phone=test_user_01.get('home_phone', ''),
        mobile_phone=test_user_01.get('mobile_phone', ''),
        work_phone=test_user_01.get('work_phone', ''),
        address_line_1=test_user_01.get('address_line_1', ''),
        address_line_2=test_user_01.get('address_line_2', ''),
        city=test_user_01.get('city', ''),
        state=test_user_01.get('state', ''),
        postal_code=test_user_01.get('postal_code', ''),
        country=test_user_01.get('country', ''),
        timezone=test_user_01.get('timezone', ''),
    )
    core_user_data.save()

    new_user = core_user_models.CoreUser(
        created_by_id=api_user.id,
        current=core_user_data,
        user=django_user
    )
    new_user.save()
