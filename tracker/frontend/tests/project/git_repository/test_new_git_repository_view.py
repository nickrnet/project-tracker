from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData

from frontend.forms.project.git_repository.new_git_repository_form import NewGitRepositoryForm


class TestNewGitRepositoryView(TestCase):
    def setUp(self):
        """
        Creates 1 user.
        """

        # TODO: BUG in the git repositories table template if the timezone is missing...
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

        self.http_client = Client()

    def test_new_git_repository_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('new_git_repository'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/new_git_repository')

    def test_new_git_repository_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('new_git_repository'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/git_repository/new_git_repository_modal.html')

    def test_new_git_repository_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        git_repository_form_data = {
            'name': 'Git Repository 1',
            'description': 'Initial Repo 1 Description',
            'url': 'https://github.com/nickrnet/project-tracker'
        }
        git_repository_form = NewGitRepositoryForm(git_repository_form_data)
        git_repository_form.is_valid()
        form_data = urlencode(git_repository_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_git_repository'), form_data, url_encoding)
        git_repository = GitRepository.objects.first()
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, '/git_repository/' + str(git_repository.id) + '/')
        # Make sure the whole form came through to the database
        self.assertEqual(git_repository.current.name, 'Git Repository 1')
        self.assertEqual(git_repository.current.description, 'Initial Repo 1 Description')
        self.assertEqual(git_repository.current.url, 'https://github.com/nickrnet/project-tracker')
        self.assertIn('Your git repository was successfully added!', str(messages))

    def test_new_git_repository_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_git_repository'), form_data, url_encoding)
        self.assertRedirects(response, reverse('new_git_repository'))
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(GitRepository.objects.count(), 0)
        self.assertIn('Error saving git repository.', str(messages))
