from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData


class TestGitRepositoriesView(TestCase):
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

    def test_git_repositories_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('git_repositories'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/git_repositories')

    def test_git_repositories_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('git_repositories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/git_repository/git_repositories_template.html')
