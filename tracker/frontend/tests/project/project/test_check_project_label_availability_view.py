from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models.user import CoreUser
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData


class TestCheckProjectLabelAvailabilityView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 project.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})

        self.project1_label_data = ProjectLabelData.objects.create(
            created_by=self.user1,
            label='project01',
            description='Project 01 Label'
        )
        self.project1_label = ProjectLabel.objects.create(created_by=self.user1, current=self.project1_label_data)

        self.project1_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project 1",
            description="Initial Project 1 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label = self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.http_client = Client()

    def test_check_project_label_availability_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('check_project_label_availability'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/check_project_label_availability/')

    def test_check_project_label_availability_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('check_project_label_availability'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context.get('unavailable'))

    def test_check_project_label_availability_view_post_returns_available(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'label=aa'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('check_project_label_availability'), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('available'))

    def test_check_project_label_availability_view_post_returns_unavailable(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'label=project01'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('check_project_label_availability'), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context.get('available'))

    def test_check_project_label_availability_view_post_returns_unavailable_for_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('check_project_label_availability'), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context.get('available'))
