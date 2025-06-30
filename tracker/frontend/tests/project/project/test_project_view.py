from datetime import datetime

from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData

from frontend.forms.project.project.project_form import ProjectDataForm


class TestProjectView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 project with label.
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

        self.http_client = Client()

    def test_project_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('project', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project/' + str(self.project1.id) + '/')

    def test_project_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_template.html')

    def test_project_view_get_with_bad_project_label(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project', kwargs={'project_id': 'wakarusa'}))
        self.assertRedirects(response, reverse('projects'))
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(ProjectData.objects.count(), 1)
        self.assertIn('The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.', str(messages))

    def test_project_view_get_with_bad_project_id(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project', kwargs={'project_id': 'e1b8f6ae-1b51-40ba-88d0-3d79bb9e9c6e'}))
        self.assertRedirects(response, reverse('projects'))
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(ProjectData.objects.count(), 1)
        self.assertIn('The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.', str(messages))
