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
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label=self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.http_client = Client()

    def test_project_settings_new_git_repository_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('project_settings_new_git_repository', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project-settings/new-git-repository/' + str(self.project1.id) + '/')

    def test_project_settings_new_git_repository_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_new_git_repository', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_new_git_repository_modal.html')

    def test_project_settings_new_git_repository_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        git_repository_form_data = {
            'name': 'Git Repository 1',
            'description': 'Initial Repo 1 Description',
            'url': 'https://github.com/nickrnet/project-tracker',
            'project_id': str(self.project1.id)
            }
        git_repository_form = NewGitRepositoryForm(git_repository_form_data)
        git_repository_form.is_valid()
        form_data = urlencode(git_repository_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_new_git_repository', kwargs={'project_id': self.project1.label.current.label}), form_data, url_encoding)
        git_repository = GitRepository.objects.first()
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        # Make sure the whole form came through to the database
        self.assertEqual(git_repository.current.name, 'Git Repository 1')
        self.assertEqual(git_repository.current.description, 'Initial Repo 1 Description')
        self.assertEqual(git_repository.current.url, 'https://github.com/nickrnet/project-tracker')
        self.assertEqual(git_repository.project_set.first(), self.project1)
        self.assertIn('Your git repository was successfully added!', str(messages))

    def test_project_settings_git_repository_view_post_to_project_without_label(self):
        self.project1.label = None
        self.project1.save()
        url_encoding = 'application/x-www-form-urlencoded'
        git_repository_form_data = {
            'name': 'Git Repository 1 Modified',
            'description': 'Initial Repo 1 Description Modified',
            'url': 'https://github.com/nickrnet/project-tracker',
            'project_id': str(self.project1.id)
            }
        git_repository_form = NewGitRepositoryForm(git_repository_form_data)
        git_repository_form.is_valid()
        form_data = urlencode(git_repository_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_new_git_repository', kwargs={'project_id': str(self.project1.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        git_repository = GitRepository.objects.first()
        self.assertEqual(git_repository.current.name, 'Git Repository 1 Modified')
        self.assertEqual(git_repository.current.description, 'Initial Repo 1 Description Modified')
        self.assertEqual(git_repository.current.url, 'https://github.com/nickrnet/project-tracker')
        self.assertIn('Your git repository was successfully added!', str(messages))

    def test_project_settings_new_git_repository_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1&project_id=' + self.project1.label.current.label
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_new_git_repository', kwargs={'project_id': str(self.project1.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(GitRepository.objects.count(), 0)
        self.assertIn('Error saving git repository.', str(messages))

    def test_project_settings_new_git_repository_view_post_with_bad_project_label(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1&project_id=wakarusa'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_new_git_repository', kwargs={'project_id': 'wakarusa'}), form_data, url_encoding)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(GitRepository.objects.count(), 0)
        self.assertIn('Error saving git repository.', str(messages))
