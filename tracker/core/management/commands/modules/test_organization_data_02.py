from core.models import user as core_user_models
from core.models import organization as core_organization_models
from .test_user_data_02 import test_user_02


test_organization_02 = {
    'name': 'Test Organization 02',
    'description': 'This is a test organization.',
    'address_line_1': '123 Main St',
    'address_line_2': '',
    'city': 'Anytown',
    'state': 'NY',
    'postal_code': '12345',
    'country': 'USA',
    'timezone': 'America/New_York',
    'responsible_party_email': test_user_02.get('email'),
    'responsible_party_phone': test_user_02.get('work_phone'),
    'is_paid': False,
    'renewal_date': None,
    'number_users_allowed': 5
}


def initialize_test_organization_02():
    test_user_02_instance = core_user_models.CoreUser.objects.get(user__email=test_user_02.get('email'))

    core_organization_data = core_organization_models.OrganizationData(
        created_by_id=test_user_02_instance.id,
        name=test_organization_02.get('name', ''),
        address_line_1=test_organization_02.get('address_line_1', ''),
        address_line_2=test_organization_02.get('address_line_2', ''),
        city=test_organization_02.get('city', ''),
        state=test_organization_02.get('state', ''),
        postal_code=test_organization_02.get('postal_code', ''),
        country=test_organization_02.get('country', ''),
        timezone=test_organization_02.get('timezone', ''),
        responsible_party_email=test_organization_02.get('responsible_party_email'),
        responsible_party_phone=test_organization_02.get('responsible_party_phone'),
    )
    core_organization_data.save()
    new_organization = core_organization_models.Organization(
        created_by_id=test_user_02_instance.id,
        current=core_organization_data,
    )
    new_organization.save()
    new_organization.members.add(test_user_02_instance)
    new_organization.save()
    test_user_02_instance.organizations.add(new_organization)
    test_user_02_instance.save()
