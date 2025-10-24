from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from core.models.user import CoreUser
from core.models.organization import Organization, OrganizationData


class TestOrganizationSettingsUserSelectView(TestCase):
    def setUp(self):
        """
        Creates 2 users, 2 organizations.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})
        self.user2 = CoreUser.objects.create_core_user_from_web({'email': 'testuser2@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

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

        self.organization2_data = OrganizationData.objects.create(
            created_by_id=self.user2.id,
            name='Test Organization 2',
            address_line_1='123 Main St',
            address_line_2='',
            city='Anytown',
            state='NY',
            postal_code='12345',
            country='USA',
            timezone='America/Chicago',
            responsible_party_email=self.user2.current.email,
            responsible_party_phone=self.user2.current.work_phone,
            )
        self.organization2 = Organization.objects.create(
            created_by_id=self.user2.id,
            current=self.organization2_data,
            )
        self.organization2.members.add(self.user2)
        self.organization2.save()

        self.http_client = Client()

    def test_organization_settings_user_select_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('organization_settings_user_select', kwargs={'organization_id': str(self.organization1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/' + str(self.organization1.id) + '/organization-settings/user-select/')

    def test_organization_settings_user_select_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('organization_settings_user_select', kwargs={'organization_id': str(self.organization1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_settings_user_select_modal.html')

    def test_organization_settings_user_select_view_get_with_bad_organization_id(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('organization_settings_user_select', kwargs={'organization_id': '4e6089a5-c16d-4642-8576-62204be7cc13'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('The specified organization does not exist. Create it and try again.', str(messages))

    def test_organization_settings_user_select_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'current_users=' + str(self.user1.id) + '&current_users=' + str(self.user2.id)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('organization_settings_user_select', kwargs={'organization_id': str(self.organization1.id)}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_users_table.html')
        # Make sure the form came through to the database and only changed the organization users
        self.organization1.refresh_from_db()
        self.assertEqual(self.organization1.current.name, 'Test Organization 1')
        self.assertEqual(self.organization1.members.count(), 2)
        self.assertIn(self.user1, self.organization1.members.all())
        self.assertIn(self.user2, self.organization1.members.all())
        self.assertIn('Organization users updated successfully!', str(messages))

    def test_organization_settings_user_select_view_post_with_invalid_users(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'current_users=b5de211e-97f1-4119-98df-5827d56ca12f&current_users=39f44dc9-5d81-4e57-a4f7-559d0f89a245'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('organization_settings_user_select', kwargs={'organization_id': self.organization1.id}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_users_table.html')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.organization1.refresh_from_db()
        self.assertEqual(self.organization1.members.count(), 1)  # Users were not added/removed
        self.assertIn(self.user1, self.organization1.members.all())
        self.assertNotIn(self.user2, self.organization1.members.all())
        self.assertIn('Could not add b5de211e-97f1-4119-98df-5827d56ca12f to organization users.', str(messages))

    def test_organization_settings_user_select_view_post_empty_list(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('organization_settings_user_select', kwargs={'organization_id': str(self.organization1.id)}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_users_table.html')
        # Make sure the form came through to the database and only changed the organization users
        self.organization1.refresh_from_db()
        self.assertEqual(self.organization1.current.name, 'Test Organization 1')
        self.assertEqual(self.organization1.members.count(), 0)
        self.assertNotIn(self.user1, self.organization1.members.all())
        self.assertNotIn(self.user2, self.organization1.members.all())
        self.assertIn('Organization users updated successfully!', str(messages))

    def test_organization_settings_user_select_view_post_to_different_organization(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'current_users=' + str(self.user2.id)
        self.http_client.force_login(user=self.user2.user)
        response = self.http_client.post(reverse('organization_settings_user_select', kwargs={'organization_id': str(self.organization1.id)}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('The specified organization does not exist. Create it and try again.', str(messages))
        # Make sure the form came through to the database and did not change the organization users
        self.organization1.refresh_from_db()
        self.assertEqual(self.organization1.current.name, 'Test Organization 1')
        self.assertEqual(self.organization1.members.count(), 1)
        self.assertIn(self.user1, self.organization1.members.all())
        self.assertNotIn(self.user2, self.organization1.members.all())
