from django.test import TestCase
from rest_framework.test import APIClient

from core.models import organization as core_organization_models
from project.models import git_repository as git_repository_models
from project.models import project as project_models
from core.models import user as core_user_models


class APITestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient(enforce_csrf_checks=True)

        # TODO: Abstract this into a helper function for use in _all_ tests
        self.api_user = core_user_models.CoreUser.objects.get_or_create_api_user()
        self.system_user = core_user_models.CoreUser.objects.get_or_create_system_user()
        self.api_test_user = core_user_models.CoreUser.objects.create_core_user_from_web({
            "email": "api_test_user_01@project-tracker.dev",
            "password": "password",
            "first_name": "API",
            "last_name": "Test User 01",
        })
        self.test_organization_data = core_organization_models.OrganizationData(
            created_by=self.api_test_user,
            name="Test Organization 01",
            description="Test Organization 01 Description",
            responsible_party_email="api_test_user_01@project-tracker.dev",
            responsible_party_phone="1234567890",
            address_line_1="123 Test St",
            postal_code="12345",
            city="Test City",
            state="Test State",
            country="Test Country"
        )
        self.test_organization_data.save()
        self.test_organization = core_organization_models.Organization(
            created_by=self.api_test_user,
            current=self.test_organization_data
        )
        self.test_organization.save()
        self.test_git_respository_data = git_repository_models.GitRepositoryData(
            created_by=self.api_test_user,
            name="Test Git Repository 01",
            description="Test Git Repository 01 Description",
            url="https://github.com/nickrnet/project-tracker"
        )
        self.test_git_respository_data.save()
        self.test_git_respository = git_repository_models.GitRepository(
            created_by=self.api_test_user,
            current=self.test_git_respository_data
        )
        self.test_git_respository.save()
        self.test_project_data = project_models.ProjectData(
            created_by=self.api_test_user,
            name="Test Project 01",
            description="Test Project 01 Description",
        )
        self.test_project_data.save()
        self.test_project = project_models.Project(
            created_by=self.api_test_user,
            current=self.test_project_data,
        )
        self.test_project.save()

        self.test_project.users.add(self.api_test_user.id)
        self.test_project.git_repository.add(self.test_git_respository)
        self.test_project.save()
        self.test_organization.members.add(self.api_test_user)
        self.test_organization.projects.add(self.test_project)
        self.test_organization.repositories.add(self.test_git_respository)
        self.test_organization.save()
        self.api_test_user.git_repositories.add(self.test_git_respository)
        self.api_test_user.projects.add(self.test_project)
        self.api_test_user.organizations.add(self.test_organization)
        self.api_test_user.save()

    # TODO: Component, Issue, IssuePriority, IssueSeverity, IssueStatus, IssueType, Version tests
    # TODO: Tests with multiple users to check for cross-user data leakage

    def test_api_get_git_repositories(self):
        # Make sure we must be authed
        response = self.api_client.get('/api/git_repositories/')
        self.assertIsNot(response.status_code, 200)
        # Auth and validate
        self.api_client.login(username=self.api_test_user.user.username, password='password')
        response = self.api_client.get('/api/git_repositories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_api_get_organizations(self):
        response = self.api_client.get('/api/organizations/')
        self.assertIsNot(response.status_code, 200)
        self.api_client.login(username=self.api_test_user.user.username, password='password')
        response = self.api_client.get('/api/organizations/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_api_get_projects(self):
        response = self.api_client.get('/api/projects/')
        self.assertIsNot(response.status_code, 200)
        self.api_client.login(username=self.api_test_user.user.username, password='password')
        response = self.api_client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_api_get_users(self):
        response = self.api_client.get('/api/users/')
        self.assertIsNot(response.status_code, 200)
        self.api_client.login(username=self.api_test_user.user.username, password='password')
        response = self.api_client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)  # api_test_user can only see themselves
        # TODO: Tests with multiple users to check for cross-user data leakage
