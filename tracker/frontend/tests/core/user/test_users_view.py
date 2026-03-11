from django.test import Client
from django.test import TestCase
from django.urls import reverse
from core.models.user import CoreUser


class TestUsersView(TestCase):
    def setUp(self):
        """
        Creates 2 users.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        self.user2 = CoreUser.objects.create_core_user_from_web({'email': 'testuser2@project-tracker.dev', 'password': 'password'})

        self.http_client = Client()

    def test_user_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('users'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/users')

    def test_user_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/users_template.html')
