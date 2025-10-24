from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from core.models.user import CoreUser

from frontend.forms.core.user.new_user_form import NewUserForm


class TestUserView(TestCase):
    def setUp(self):
        """
        Creates 1 user.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})

        self.http_client = Client()

    def test_user_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('user', kwargs={'user_id': self.user1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/user/' + str(self.user1.id) + '/')

    def test_user_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('user', kwargs={'user_id': self.user1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/core_user_template.html')

    def test_user_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        user_form_data = {
            'email': 'testuser1+modified@project-tracker.dev',
            'name_prefix': 'Prefix',
            'first_name': 'Test',
            'middle_name': '1',
            'last_name': 'User',
            'name_suffix': 'Suffix',
            'secondary_email': 'testuser1+secondary_modified@project-tracker.dev',
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
        user_form = NewUserForm(user_form_data)
        user_form.is_valid()
        form_data = urlencode(user_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('user', kwargs={'user_id': self.user1.id}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        # Get the user we just created for checking
        user = CoreUser.objects.get(current__email='testuser1+modified@project-tracker.dev')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/' + str(user.id) + '/')
        # Make sure the whole form came through to the database
        self.assertEqual(user.current.name_prefix, 'Prefix')
        self.assertEqual(user.current.first_name, 'Test')
        self.assertEqual(user.current.middle_name, '1')
        self.assertEqual(user.current.last_name, 'User')
        self.assertEqual(user.current.name_suffix, 'Suffix')
        self.assertEqual(user.current.email, 'testuser1+modified@project-tracker.dev')
        self.assertEqual(user.current.secondary_email, 'testuser1+secondary_modified@project-tracker.dev')
        self.assertEqual(user.current.address_line_1, '1234 Tomato Ln')
        self.assertEqual(user.current.address_line_2, 'n/a')
        self.assertEqual(user.current.postal_code, '12345')
        self.assertEqual(user.current.city, 'Anytown')
        self.assertEqual(user.current.state, 'NY')
        self.assertEqual(user.current.country, 'US')
        self.assertEqual(user.current.timezone, 'EST')
        self.assertIn('Your user was successfully updated!', str(messages))

    def test_user_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('user', kwargs={'user_id': self.user1.id}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/' + str(self.user1.id) + '/')
        self.assertIn('Error saving user.', str(messages))
