from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from core.models.user import CoreUser, UserLogin

from frontend.forms.login_form import LoginForm


class TestLoginView(TestCase):
    def setUp(self):
        """
        Creates 1 user.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})

        self.http_client = Client(headers={"user-agent": 'Mozilla/5.0'})

    def test_login_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('login_template.html')

    def test_login_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        login_form_data = {
            'email': 'testuser1@project-tracker.dev',
            'password': 'password'
            }
        login_form = LoginForm(login_form_data)
        login_form.is_valid()
        form_data = urlencode(login_form.data)
        response = self.http_client.post(reverse('login'), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, '/projects')
        self.assertIn('You were successfully logged in!', str(messages))
        self.assertEqual(1, UserLogin.objects.count())

    def test_login_view_post_with_unknown_user(self):
        url_encoding = 'application/x-www-form-urlencoded'
        login_form_data = {
            'email': 'testuser2@project-tracker.dev',
            'password': 'password'
            }
        login_form = LoginForm(login_form_data)
        login_form.is_valid()
        form_data = urlencode(login_form.data)
        response = self.http_client.post(reverse('login'), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_template.html')
        self.assertIn('Error logging in.', str(messages))
        self.assertEqual(0, UserLogin.objects.count())

    def test_login_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'a=b'
        response = self.http_client.post(reverse('login'), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_template.html')
        self.assertIn('Error logging in.', str(messages))
        self.assertEqual(0, UserLogin.objects.count())
