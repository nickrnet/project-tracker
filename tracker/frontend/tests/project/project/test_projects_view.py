from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models.user import CoreUser
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData


class TestProjectsView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 2 projects with labels.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

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
            is_active=True,
            is_private=False
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label=self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.project2_label_data = ProjectLabelData.objects.create(
            created_by=self.user1,
            label='project02',
            description='Project 02 Label'
            )
        self.project2_label = ProjectLabel.objects.create(created_by=self.user1, current=self.project2_label_data)

        self.project2_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project 2",
            description="Initial Project 2 Description",
            start_date=timezone.now(),
            is_active=True,
            is_private=False
            )
        self.project2 = Project.objects.create(created_by=self.user1, current=self.project2_data, label=self.project2_label)
        self.project2.users.add(self.user1)
        self.project2.save()

        self.http_client = Client()

    def test_projects_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('projects'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/projects')

    def test_projects_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/projects_template.html')
