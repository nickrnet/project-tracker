from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser

from frontend.forms.core.organization.organization_form import OrganizationDataForm


class TestOrganizationView(TestCase):
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

    def test_organization_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('organization', kwargs={'organization_id': str(self.organization1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/organization/' + str(self.organization1.id) + '/')

    def test_organization_view_redirects_when_unknown_user_logs_in(self):
        response = self.http_client.get(reverse('organization', kwargs={'organization_id': str(self.organization1.id)}), HTTP_AUTHORIZATION='Basic john.smith:secret')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/organization/' + str(self.organization1.id) + '/')

    def test_organization_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('organization', kwargs={'organization_id': str(self.organization1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_template.html')
        
    def test_organization_view_get_with_bad_organization_id(self):
        bad_uuid = '4af0c4fd-839a-4403-bf2d-e4204b9dab79'
        url_encoding = 'application/x-www-form-urlencoded'
        new_organization_form_data = {
            'name': 'Organization 1 Modified',
            'description': 'Organization 1 Modified Description',
            'responsible_party_email': 'organization1modified@project-tracker.dev',
            'responsible_party_phone': '555-555-9999',
            'address_line_1': '12345678 Tomato Ln',
            'city': 'Anytown Modified',
            'state': 'NJ',
            'postal_code': 12346,
            'country': 'US',
            'timezone': 'EST',
            'is_paid': True,
            'renewal_date': '',
        }
        organization_form = OrganizationDataForm(new_organization_form_data)
        organization_form.is_valid()
        form_data = urlencode(organization_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('organization', kwargs={'organization_id': bad_uuid}), form_data, url_encoding)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('organizations'))

    def test_organization_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        new_organization_form_data = {
            'name': 'Organization 1 Modified',
            'description': 'Organization 1 Modified Description',
            'responsible_party_email': 'organization1modified@project-tracker.dev',
            'responsible_party_phone': '555-555-9999',
            'address_line_1': '12345678 Tomato Ln',
            'city': 'Anytown Modified',
            'state': 'NJ',
            'postal_code': 12346,
            'country': 'US',
            'timezone': 'EST',
            'is_paid': True,
            'renewal_date': '',
            'number_users_allowed': 1000
        }
        organization_form = OrganizationDataForm(new_organization_form_data)
        organization_form.is_valid()
        form_data = urlencode(organization_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('organization', kwargs={'organization_id': str(self.organization1.id)}), form_data, url_encoding)
        self.organization1.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organization/' + str(self.organization1.id) + '/')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.assertEqual(self.organization1.current.name, 'Organization 1 Modified')
        self.assertEqual(self.organization1.current.description, 'Organization 1 Modified Description')
        self.assertEqual(self.organization1.current.responsible_party_email, 'organization1modified@project-tracker.dev')
        self.assertEqual(self.organization1.current.responsible_party_phone, '555-555-9999')
        self.assertEqual(self.organization1.current.address_line_1, '12345678 Tomato Ln')
        self.assertEqual(self.organization1.current.city, 'Anytown Modified')
        self.assertEqual(self.organization1.current.state, 'NJ')
        self.assertEqual(self.organization1.current.postal_code, '12346')
        self.assertEqual(self.organization1.current.country, 'US')
        self.assertEqual(self.organization1.current.timezone, 'EST')
        self.assertEqual(self.organization1.current.is_paid, True)
        self.assertEqual(self.organization1.current.renewal_date, None)
        self.assertEqual(self.organization1.current.number_users_allowed, 1000)
        self.assertIn('Your organization was successfully updated!', str(messages))

    def test_organization_view_post_without_number_users_allowed(self):
        url_encoding = 'application/x-www-form-urlencoded'
        new_organization_form_data = {
            'name': 'Organization 1 Modified',
            'description': 'Organization 1 Modified Description',
            'responsible_party_email': 'organization1modified@project-tracker.dev',
            'responsible_party_phone': '555-555-9999',
            'address_line_1': '12345678 Tomato Ln',
            'city': 'Anytown Modified',
            'state': 'NJ',
            'postal_code': 12346,
            'country': 'US',
            'timezone': 'EST',
            'is_paid': True,
            'renewal_date': '',
        }
        organization_form = OrganizationDataForm(new_organization_form_data)
        organization_form.is_valid()
        form_data = urlencode(organization_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('organization', kwargs={'organization_id': str(self.organization1.id)}), form_data, url_encoding)
        self.organization1.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organization/' + str(self.organization1.id) + '/')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.assertEqual(self.organization1.current.name, 'Organization 1 Modified')
        self.assertEqual(self.organization1.current.description, 'Organization 1 Modified Description')
        self.assertEqual(self.organization1.current.responsible_party_email, 'organization1modified@project-tracker.dev')
        self.assertEqual(self.organization1.current.responsible_party_phone, '555-555-9999')
        self.assertEqual(self.organization1.current.address_line_1, '12345678 Tomato Ln')
        self.assertEqual(self.organization1.current.city, 'Anytown Modified')
        self.assertEqual(self.organization1.current.state, 'NJ')
        self.assertEqual(self.organization1.current.postal_code, '12346')
        self.assertEqual(self.organization1.current.country, 'US')
        self.assertEqual(self.organization1.current.timezone, 'EST')
        self.assertEqual(self.organization1.current.is_paid, True)
        self.assertEqual(self.organization1.current.renewal_date, None)
        self.assertIn('Your organization was successfully updated!', str(messages))

    def test_organization_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('organization', kwargs={'organization_id': str(self.organization1.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organization/' + str(self.organization1.id) + '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Error updating organization.', str(messages))
