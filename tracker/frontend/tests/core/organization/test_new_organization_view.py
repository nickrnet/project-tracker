from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from core.models.organization import Organization
from core.models.user import CoreUser

from frontend.forms.core.organization.new_organization_form import NewOrganizationDataForm


class TestNewOrganizationView(TestCase):
    def setUp(self):
        """
        Creates 1 user.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})

        self.http_client = Client()

    def test_new_organization_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('new_organization'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/new_organization')

    def test_new_organization_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('new_organization'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/new_organization_modal.html')

    def test_new_organization_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        new_organization_form_data = {
            'name': 'Organization 1',
            'description': 'Organization 1 Description',
            'responsible_party_email': 'organization1@project-tracker.dev',
            'responsible_party_phone': '555-555-1111',
            'address_line_1': '1234 Tomato Ln',
            'city': 'Anytown',
            'state': 'NY',
            'postal_code': 12345,
            'country': 'US',
            'timezone': 'EST',
            'is_paid': True,
            'renewal_date': '',
            'number_users_allowed': 1000
        }
        new_organization_form = NewOrganizationDataForm(new_organization_form_data)
        new_organization_form.is_valid()
        form_data = urlencode(new_organization_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_organization'), form_data, url_encoding)
        # Get the organization we just created for checking
        organization = Organization.objects.get(current__responsible_party_email='organization1@project-tracker.dev')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organization/' + str(organization.id) + '/')
        # Make sure the whole form came through to the database
        self.assertEqual(organization.current.name, 'Organization 1')
        self.assertEqual(organization.current.description, 'Organization 1 Description')
        self.assertEqual(organization.current.responsible_party_email, 'organization1@project-tracker.dev')
        self.assertEqual(organization.current.responsible_party_phone, '555-555-1111')
        self.assertEqual(organization.current.address_line_1, '1234 Tomato Ln')
        self.assertEqual(organization.current.city, 'Anytown')
        self.assertEqual(organization.current.state, 'NY')
        self.assertEqual(organization.current.postal_code, '12345')
        self.assertEqual(organization.current.country, 'US')
        self.assertEqual(organization.current.timezone, 'EST')
        self.assertEqual(organization.current.is_paid, True)
        self.assertEqual(organization.current.renewal_date, None)
        self.assertEqual(organization.current.number_users_allowed, 1000)

    def test_new_organization_view_post_without_number_users_allowed(self):
        url_encoding = 'application/x-www-form-urlencoded'
        new_organization_form_data = {
            'name': 'Organization 1',
            'description': 'Organization 1 Description',
            'responsible_party_email': 'organization1@project-tracker.dev',
            'responsible_party_phone': '555-555-1111',
            'address_line_1': '1234 Tomato Ln',
            'city': 'Anytown',
            'state': 'NY',
            'postal_code': 12345,
            'country': 'US',
            'timezone': 'EST',
            'is_paid': True,
            'renewal_date': ''
        }
        new_organization_form = NewOrganizationDataForm(new_organization_form_data)
        new_organization_form.is_valid()
        form_data = urlencode(new_organization_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_organization'), form_data, url_encoding)
        # Get the organization we just created for checking
        organization = Organization.objects.get(current__responsible_party_email='organization1@project-tracker.dev')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organization/' + str(organization.id) + '/')
        # Make sure the whole form came through to the database
        self.assertEqual(organization.current.name, 'Organization 1')
        self.assertEqual(organization.current.description, 'Organization 1 Description')
        self.assertEqual(organization.current.responsible_party_email, 'organization1@project-tracker.dev')
        self.assertEqual(organization.current.responsible_party_phone, '555-555-1111')
        self.assertEqual(organization.current.address_line_1, '1234 Tomato Ln')
        self.assertEqual(organization.current.city, 'Anytown')
        self.assertEqual(organization.current.state, 'NY')
        self.assertEqual(organization.current.postal_code, '12345')
        self.assertEqual(organization.current.country, 'US')
        self.assertEqual(organization.current.timezone, 'EST')
        self.assertEqual(organization.current.is_paid, True)
        self.assertEqual(organization.current.renewal_date, None)
        self.assertEqual(organization.current.number_users_allowed, 5)

    def test_new_organization_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_organization'), form_data, url_encoding)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
