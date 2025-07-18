from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from core.models.user import CoreUser, UserLogout


class TestLogoutView(TestCase):
    def setUp(self):
        """
        Creates 1 user.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})

        self.http_client = Client(headers={"user-agent": 'Mozilla/5.0'})

    def test_logout_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('logout'))
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, '/login')
        self.assertIn('You were successfully logged out!', str(messages))
        self.assertEqual(1, UserLogout.objects.count())
        # Make sure session stuff is really gone in the client
        response = self.http_client.get(reverse('projects'))
        self.assertRedirects(response, '/login?next=/projects')
