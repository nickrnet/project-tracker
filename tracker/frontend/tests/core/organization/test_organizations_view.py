from django.test import Client
from django.test import TestCase
from django.urls import reverse

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser


class TestOrganizationsView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 organization.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})

        self.organization1_data = OrganizationData.objects.create(
            created_by_id=self.user1.id,
            name='Test Organization 1',
            address_line_1='123 Main St',
            address_line_2='',
            city='Anytown',
            state='NY',
            postal_code='12345',
            country='USA',
            timezone='America/Chicago',
            responsible_party_email=self.user1.current.email,
            responsible_party_phone=self.user1.current.work_phone,
            )
        self.organization1 = Organization.objects.create(
            created_by_id=self.user1.id,
            current=self.organization1_data,
            )
        self.organization1.members.add(self.user1)
        self.organization1.save()

        self.http_client = Client()

    def test_organizations_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('organizations'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/organizations')

    def test_organizations_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('organizations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organizations_template.html')
