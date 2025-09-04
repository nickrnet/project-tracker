from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from core.models.user import CoreUser, UserLogin

from frontend.forms.signup_form import SignupForm


class TestSignupView(TestCase):
    def setUp(self):
        """
        Creates an HTTP client.
        """

        self.http_client = Client(headers={"user-agent": 'Mozilla/5.0'})

    def test_signup_view_get(self):
        response = self.http_client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('signup_template.html')

    def test_signup_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        login_form_data = {
            'email': 'testuser1@project-tracker.dev',
            'password': 'password',
            'name_prefix': 'Prefix',
            'first_name': 'Test',
            'middle_name': '1',
            'last_name': 'User',
            'name_suffix': 'Suffix',
            'secondary_email': 'testuser1+secondary@project-tracker.dev',
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
        login_form = SignupForm(login_form_data)
        login_form.is_valid()
        form_data = urlencode(login_form.data)
        response = self.http_client.post(reverse('signup'), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('login'))
        self.assertIn('Your signup was successful!', str(messages))
        self.assertEqual(2, CoreUser.objects.count())  # API System User also exists
        # Make sure the whole form came through to the database
        user = CoreUser.objects.get(current__email='testuser1@project-tracker.dev')
        self.assertEqual(user.current.name_prefix, 'Prefix')
        self.assertEqual(user.current.first_name, 'Test')
        self.assertEqual(user.current.middle_name, '1')
        self.assertEqual(user.current.last_name, 'User')
        self.assertEqual(user.current.name_suffix, 'Suffix')
        self.assertEqual(user.current.email, 'testuser1@project-tracker.dev')
        self.assertEqual(user.current.secondary_email, 'testuser1+secondary@project-tracker.dev')
        self.assertEqual(user.current.address_line_1, '1234 Tomato Ln')
        self.assertEqual(user.current.address_line_2, 'n/a')
        self.assertEqual(user.current.postal_code, '12345')
        self.assertEqual(user.current.city, 'Anytown')
        self.assertEqual(user.current.state, 'NY')
        self.assertEqual(user.current.country, 'US')
        self.assertEqual(user.current.timezone, 'EST')

    def test_signup_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'a=b'
        response = self.http_client.post(reverse('signup'), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_template.html')
        self.assertIn('Error saving user. Double check your data and try again.', str(messages))
        self.assertEqual(0, UserLogin.objects.count())
