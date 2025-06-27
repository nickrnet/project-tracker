from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData

from frontend.forms.project.git_repository.git_repository_form import GitRepositoryDataForm


class TestGitRepositoryView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 git repository.
        """

        self.system_user = CoreUser.objects.get_or_create_system_user()
        # TODO: BUG in the git repositories table template if the timezone is missing...
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

        self.git_repository1_data = GitRepositoryData.objects.create(
            created_by=self.user1,
            name="Initial Repo 1",
            description="Initial Repo 1 Description",
            url="https://github.com/example/repo1"
            )
        self.git_repository1_data.save()
        self.git_repository1 = GitRepository.objects.create(created_by=self.user1, current=self.git_repository1_data)

        self.http_client = Client()

    def test_git_repository_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/git_repository/' + str(self.git_repository1.id) + '/')

    def test_git_repository_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/git_repository/git_repository_modal.html')

    def test_git_repository_view_post(self):
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
        response = self.http_client.post(reverse('git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}), form_data, url_encoding)
        self.assertRedirects(response, '/git_repository/' + str(self.git_repository1.id) + '/')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.git_repository1.refresh_from_db()
        self.assertEqual(self.git_repository1.current.name, 'Git Repository 1 Modified')
        self.assertEqual(self.git_repository1.current.description, 'Initial Repo 1 Description Modified')
        self.assertEqual(self.git_repository1.current.url, 'https://github.com/nickrnet/project-tracker')
        self.assertIn('Your git repository was successfully updated!', str(messages))

    def test_git_repository_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}), form_data, url_encoding)
        self.assertRedirects(response, '/git_repository/' + str(self.git_repository1.id) + '/')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.git_repository1.refresh_from_db()
        self.assertEqual(self.git_repository1.current.name, 'Initial Repo 1')
        self.assertEqual(self.git_repository1.current.description, 'Initial Repo 1 Description')
        self.assertEqual(self.git_repository1.current.url, 'https://github.com/example/repo1')
        self.assertIn('Error saving git repository.', str(messages))

    def test_git_repository_view_get_url_validator(self):
        self.http_client.force_login(user=self.user1.user)
        self.git_repository1.current.url = "aaa:/b}}}"
        self.git_repository1.current.save()
        response = self.http_client.get(reverse('git_repository', kwargs={'git_repository_id': str(self.git_repository1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/git_repository/git_repository_modal.html')
        self.assertFalse(response.context.get('valid_url'))
