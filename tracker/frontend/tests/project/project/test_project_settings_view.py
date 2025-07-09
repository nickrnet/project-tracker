from datetime import datetime

from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData

from frontend.forms.project.project.project_form import ProjectDataForm


class TestProjectSettingsView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 project with label.
        """

        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

        self.git_repository1_data = GitRepositoryData.objects.create(
            created_by=self.user1,
            name="Initial Repo 1",
            description="Initial Repo 1 Description",
            url="https://github.com/example/repo1"
            )
        self.git_repository1_data.save()
        self.git_repository1 = GitRepository.objects.create(created_by=self.user1, current=self.git_repository1_data)

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
        self.project1.git_repositories.add(self.git_repository1)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.http_client = Client()

    def test_project_settings_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('project_settings', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project-settings/' + str(self.project1.id) + '/')

    def test_project_settings_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')

    def test_project_settings_view_post(self):
        start_date = timezone.now().strftime("%m/%d/%Y")
        end_date = timezone.now().strftime("%m/%d/%Y")
        url_encoding = 'application/x-www-form-urlencoded'
        project_form_data = {
            'name': 'Initial Project 1 Modified',
            'description': 'Initial Project 1 Description Modified',
            'label': 'project01-modified',
            'is_active': False,
            'is_private': True,
            'start_date': start_date,
            'end_date': end_date,
            }
        project_form = ProjectDataForm(project_form_data)
        project_form.is_valid()
        form_data = urlencode(project_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings', kwargs={'project_id': self.project1.label.current.label}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.project1.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/project/' + self.project1.label.current.label + '/')
        # Make sure the whole form came through to the database
        self.assertEqual(self.project1.current.name, 'Initial Project 1 Modified')
        self.assertEqual(self.project1.current.description, 'IInitial Project 1 Description Modified')
        self.assertEqual(self.project1.current.is_active, False)
        self.assertEqual(self.project1.current.is_private, True)
        self.assertEqual(self.project1.current.start_date, datetime.strptime(start_date, '%m/%d/%Y').date())
        self.assertEqual(self.project1.current.end_date, datetime.strptime(end_date, '%m/%d/%Y').date())
        self.assertIn('Your project was successfully updated!', str(messages))

    def test_project_settings_view_post_to_project_without_label(self):
        self.project1.label = None
        self.project1.save()
        start_date = timezone.now().strftime("%m/%d/%Y")
        end_date = timezone.now().strftime("%m/%d/%Y")
        url_encoding = 'application/x-www-form-urlencoded'
        project_form_data = {
            'name': 'Initial Project 1 Modified',
            'description': 'Initial Project 1 Description Modified',
            'is_active': False,
            'is_private': True,
            'start_date': start_date,
            'end_date': end_date,
            }
        project_form = ProjectDataForm(project_form_data)
        project_form.is_valid()
        form_data = urlencode(project_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings', kwargs={'project_id': self.project1.label.current.label}), form_data, url_encoding)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project', kwargs={'project_id': self.project1.label.current.label}))
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.current.name, 'Initial Project 1 Modified')
        self.assertEqual(self.project1.current.description, 'IInitial Project 1 Description Modified')
        self.assertEqual(self.project1.current.is_active, False)
        self.assertEqual(self.project1.current.is_private, True)
        self.assertEqual(self.project1.current.start_date, datetime.strptime(start_date, '%m/%d/%Y').date())
        self.assertEqual(self.project1.current.end_date, datetime.strptime(end_date, '%m/%d/%Y').date())
        self.assertIn('Your project was successfully updated!', str(messages))

    def test_project_settings_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings', kwargs={'project_id': str(self.project1.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project', kwargs={'project_id': str(self.project1.id)}))
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(ProjectData.objects.count(), 1)
        self.assertIn('Error saving project.', str(messages))

    def test_project_settings_view_post_with_bad_project_label(self):
        start_date = timezone.now().strftime("%m/%d/%Y")
        end_date = timezone.now().strftime("%m/%d/%Y")
        url_encoding = 'application/x-www-form-urlencoded'
        project_form_data = {
            'name': 'Initial Project 1 Modified',
            'description': 'Initial Project 1 Description Modified',
            'label': 'project01-modified',
            'is_active': False,
            'is_private': True,
            'start_date': start_date,
            'end_date': end_date,
            }
        project_form = ProjectDataForm(project_form_data)
        project_form.is_valid()
        form_data = urlencode(project_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings', kwargs={'project_id': 'awesome-project'}), form_data, url_encoding)
        self.assertRedirects(response, reverse('projects'))
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(ProjectData.objects.count(), 1)  # There is one ProjectData object created in setUp
        self.assertIn('The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.', str(messages))
