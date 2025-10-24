from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from core.models.user import CoreUser

from frontend.forms.core.user.new_user_form import NewUserForm


class TestNewUserView(TestCase):
    def setUp(self):
        """
        Creates 1 user.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})

        self.http_client = Client()

    def test_new_user_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('new_user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/new_user')

    def test_new_user_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('new_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/new_user_modal.html')

    def test_new_user_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        new_user_form_data = {
            'email': 'testuser2@project-tracker.dev',
            'password': 'password123',
            'name_prefix': 'Prefix',
            'first_name': 'Test',
            'middle_name': '2',
            'last_name': 'User',
            'name_suffix': 'Suffix',
            'secondary_email': 'testuser2+secondary@project-tracker.dev',
            'home_phone': '5555551111',
            'mobile_phone': '5555552222',
            'work_phone': '5555553333',
            'address_line_1': '1234 Tomato Ln',
            'address_line_2': 'n/a',
            'postal_code': 12345,
            'city': 'Anytown',
            'state': 'NY',
            'country': 'US',
            'timezone': 'EST'
        }
        new_user_form = NewUserForm(new_user_form_data)
        new_user_form.is_valid()
        form_data = urlencode(new_user_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_user'), form_data, url_encoding)
        # Get the user we just created for checking
        user = CoreUser.objects.get(current__email='testuser2@project-tracker.dev')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/' + str(user.id) + '/')
        # Make sure the whole form came through to the database
        self.assertEqual(user.current.name_prefix, 'Prefix')
        self.assertEqual(user.current.first_name, 'Test')
        self.assertEqual(user.current.middle_name, '2')
        self.assertEqual(user.current.last_name, 'User')
        self.assertEqual(user.current.name_suffix, 'Suffix')
        self.assertEqual(user.current.email, 'testuser2@project-tracker.dev')
        self.assertEqual(user.current.secondary_email, 'testuser2+secondary@project-tracker.dev')
        self.assertEqual(user.current.address_line_1, '1234 Tomato Ln')
        self.assertEqual(user.current.address_line_2, 'n/a')
        self.assertEqual(user.current.postal_code, '12345')
        self.assertEqual(user.current.city, 'Anytown')
        self.assertEqual(user.current.state, 'NY')
        self.assertEqual(user.current.country, 'US')
        self.assertEqual(user.current.timezone, 'EST')

    def test_new_user_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_user'), form_data, url_encoding)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users')
