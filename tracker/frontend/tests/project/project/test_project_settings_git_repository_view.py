from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData

from frontend.forms.project.git_repository.git_repository_form import GitRepositoryDataForm


class TestProjectSettingsGitRepositoryView(TestCase):
    def setUp(self):
        """
        Creates 2 users, 1 project, 1 git repository.
        """

        self.system_user = CoreUser.objects.get_or_create_system_user()
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})
        self.user2 = CoreUser.objects.create_core_user_from_web({'email': 'testuser2@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

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
            is_active=True
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label=self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.git_repositories.add(self.git_repository1)
        self.project1.save()

        self.http_client = Client()

    def test_project_settings_git_repository_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('project_settings_git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project-settings/git-repository/' + str(self.git_repository1.id) + '/')

    def test_project_settings_git_repository_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_git_repository_modal.html')

    def test_project_settings_git_repository_view_get_user_cannot_access_git_repository(self):
        self.http_client.force_login(user=self.user2.user)
        response = self.http_client.get(reverse('project_settings_git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')
        self.assertIn('The specified Git Repository does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.', str(messages))

    def test_project_settings_git_repository_view_get_user_cannot_access_project(self):
        self.project1.users.remove(self.user1)
        self.project1.save()
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')
        self.assertIn('The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.', str(messages))

    def test_project_settings_git_repository_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        git_repository_form_data = {
            'name': 'Git Repository 1 Modified',
            'description': 'Initial Repo 1 Description Modified',
            'url': 'https://github.com/nickrnet/project-tracker'
            }
        git_repository_form = GitRepositoryDataForm(git_repository_form_data)
        git_repository_form.is_valid()
        form_data = urlencode(git_repository_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.git_repository1.refresh_from_db()
        self.assertEqual(self.git_repository1.current.name, 'Git Repository 1 Modified')
        self.assertEqual(self.git_repository1.current.description, 'Initial Repo 1 Description Modified')
        self.assertEqual(self.git_repository1.current.url, 'https://github.com/nickrnet/project-tracker')
        self.assertIn('Your git repository was successfully updated!', str(messages))

    def test_project_settings_git_repository_view_post_to_project_without_label(self):
        self.project1.label = None
        self.project1.save()
        url_encoding = 'application/x-www-form-urlencoded'
        git_repository_form_data = {
            'name': 'Git Repository 1 Modified',
            'description': 'Initial Repo 1 Description Modified',
            'url': 'https://github.com/nickrnet/project-tracker'
            }
        git_repository_form = GitRepositoryDataForm(git_repository_form_data)
        git_repository_form.is_valid()
        form_data = urlencode(git_repository_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.git_repository1.refresh_from_db()
        self.assertEqual(self.git_repository1.current.name, 'Git Repository 1 Modified')
        self.assertEqual(self.git_repository1.current.description, 'Initial Repo 1 Description Modified')
        self.assertEqual(self.git_repository1.current.url, 'https://github.com/nickrnet/project-tracker')
        self.assertIn('Your git repository was successfully updated!', str(messages))

    def test_project_settings_git_repository_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.git_repository1.refresh_from_db()
        self.assertEqual(self.git_repository1.current.name, 'Initial Repo 1')
        self.assertEqual(self.git_repository1.current.description, 'Initial Repo 1 Description')
        self.assertEqual(self.git_repository1.current.url, 'https://github.com/example/repo1')
        self.assertIn('Error saving git repository.', str(messages))

    def test_project_settings_git_repository_view_get_url_validator(self):
        self.http_client.force_login(user=self.user1.user)
        self.git_repository1.current.url = "aaa:/b}}}"
        self.git_repository1.current.save()
        response = self.http_client.get(reverse('project_settings_git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_git_repository_modal.html')
        self.assertFalse(response.context.get('valid_url'))
