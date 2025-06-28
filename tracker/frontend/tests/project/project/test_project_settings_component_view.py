from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.git_repository import GitRepository
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData

from frontend.forms.project.git_repository.new_git_repository_form import NewGitRepositoryForm

# # Testing
# import pytest
# pytestmark = pytest.mark.rw


class TestProjectSettingsNewGitRepositoryView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 project.
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
            is_active=True
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label = self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.http_client = Client()

    def test_project_settings_component_redirects_if_not_logged_in(self):
        response = self.http_client.get(reverse('project_settings_component'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project-settings/component/')

    #TODO - current failure; find out where active components are and get id(s) to pass in as kwargs
    def test_project_settings_component_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_component'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_component_modal.html')