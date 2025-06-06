from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.issue import Issue, IssueData
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData


class CoreUserTestCase(TestCase):
    def setUp(self):
        """
        Creates 3 users, 3 organizatios, 3 projects, and 1 git repository.
        User1 is in all 3 organizations explicitly, projects 1 and 2 explicitly as a user, and project 3 by being in the organization, and owns the git repository.
        User2 is in organization 2 and project 2 explictly.
        User3 is in organization 3.
        """

        self.api_client = APIClient(enforce_csrf_checks=True)
        self.system_user = CoreUser.objects.get_or_create_system_user()

        self.user1 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        self.user2 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser2@project-tracker.dev', 'password': 'password'})
        self.user3 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser3@project-tracker.dev', 'password': 'password'})

        self.organization1_data = OrganizationData(
            created_by_id=self.user1.id,
            name='Test Organization 1',
            address_line_1='123 Main St',
            address_line_2='',
            city='Anytown',
            state='NY',
            postal_code='12345',
            country='USA',
            timezone='America/Chicago',
            responsible_party_email=self.user1.current.email,
            responsible_party_phone=self.user1.current.work_phone,
            )
        self.organization1_data.save()
        self.organization1_data.save()
        self.organization1 = Organization(
            created_by_id=self.user1.id,
            current=self.organization1_data,
            )
        self.organization1.save()
        self.organization1.members.add(self.user1)

        self.organization2_data = OrganizationData(
            created_by_id=self.user2.id,
            name='Test Organization 2',
            address_line_1='123 Main St',
            address_line_2='',
            city='Anytown',
            state='NY',
            postal_code='12345',
            country='USA',
            timezone='America/Chicago',
            responsible_party_email=self.user2.current.email,
            responsible_party_phone=self.user2.current.work_phone,
            )
        self.organization2_data.save()
        self.organization2_data.save()
        self.organization2 = Organization(
            created_by_id=self.user2.id,
            current=self.organization2_data,
            )
        self.organization2.save()
        self.organization2.members.add(self.user1, self.user2)

        self.organization3_data = OrganizationData(
            created_by_id=self.user3.id,
            name='Test Organization 3',
            address_line_1='123 Main St',
            address_line_2='',
            city='Anytown',
            state='NY',
            postal_code='12345',
            country='USA',
            timezone='America/Chicago',
            responsible_party_email=self.user3.current.email,
            responsible_party_phone=self.user3.current.work_phone,
            )
        self.organization3_data.save()
        self.organization3_data.save()
        self.organization3 = Organization(
            created_by_id=self.user3.id,
            current=self.organization3_data,
            )
        self.organization3.save()
        self.organization3.members.add(self.user1, self.user3)

        self.git_repository1_data = GitRepositoryData.objects.create(
            created_by=self.user1,
            name="Initial Repo 1",
            description="Initial Repo 1 Description",
            url="https://github.com/example/repo1"
            )
        self.git_repository1_data.save()
        self.git_repository1 = GitRepository.objects.create(
            created_by=self.user1, current=self.git_repository1_data)

        self.project1_data_label_data = ProjectLabelData(
            created_by=self.user1,
            label='project01',
            description='Project 01 Label'
        )
        self.project1_data_label_data.save()
        self.project1_data_label = ProjectLabel(
            created_by=self.user1,
            current=self.project1_data_label_data
        )
        self.project1_data_label.save()
        self.project1_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project 1",
            description="Initial Project 1 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project1_data.save()
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data)
        self.project1.label = self.project1_data_label
        self.project1.git_repositories.add(self.git_repository1)
        self.project1.users.add(self.user1)

        self.project2_data = ProjectData.objects.create(
            created_by=self.user2,
            name="Initial Project 2",
            description="Initial Project 2 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project2_data.save()
        self.project2 = Project.objects.create(created_by=self.user2, current=self.project2_data)
        self.project2.users.add(self.user1, self.user2)

        self.project3_data = ProjectData.objects.create(
            created_by=self.system_user,
            name="initialproject3",
            description="Initial Project 3 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project3_data.save()
        self.project3 = Project.objects.create(created_by=self.system_user, current=self.project3_data)
        self.organization3.projects.add(self.project3.id)
        
    def test_deactivate_login(self):
        self.user1.deactivate_login()
        self.assertEqual(self.user1.user.is_active, False)
        self.api_client.login(username=self.user1.user.username, password='password')
        response = self.api_client.get('/api/projects/')
        self.assertEqual(response.status_code, 403)

    def test_list_projects(self):
        user1_projects = self.user1.list_projects()
        user2_projects = self.user2.list_projects()
        user3_projects = self.user3.list_projects()

        self.assertEqual(len(user1_projects), 3)
        self.assertEqual(len(user2_projects), 1)
        self.assertEqual(len(user3_projects), 1)
        self.assertIn(self.project1, user1_projects)
        self.assertIn(self.project2, user1_projects)
        self.assertIn(self.project2, user2_projects)
        self.assertIn(self.project3, user3_projects)
        self.assertNotIn(self.project1, user2_projects)
        self.assertNotIn(self.project1, user3_projects)
        self.assertNotIn(self.project2, user3_projects)

    def test_list_git_repositories(self):
        user1_git_repositories = self.user1.list_git_repositories()
        user2_git_repositories = self.user2.list_git_repositories()
        user3_git_repositories = self.user3.list_git_repositories()

        self.assertEqual(len(user1_git_repositories), 1)
        self.assertEqual(len(user2_git_repositories), 0)
        self.assertEqual(len(user3_git_repositories), 0)
        self.assertIn(self.git_repository1, user1_git_repositories)
        self.assertNotIn(self.git_repository1, user2_git_repositories)
        self.assertNotIn(self.git_repository1, user3_git_repositories)

    def test_list_issues(self):
        # TODO
        issue1_data = IssueData(
            created_by=self.user1,
            summary="Test Issue 1",
            project=self.project1,
            reporter=self.user1
            )
        issue1_data.save()
        issue1 = Issue(
            created_by=self.user1,
            current=issue1_data,
            sequence=Issue.objects.get_next_sequence_number(self.project1.id)
        )
        issue1.save()
        issue2_data = IssueData(
            created_by=self.user2,
            summary="Test Issue 2",
            project=self.project2,
            reporter=self.user2
            )
        issue2_data.save()
        issue2 = Issue(
            created_by=self.user2,
            current=issue2_data,
            sequence=Issue.objects.get_next_sequence_number(self.project2.id)
        )
        issue2.save()
        issue3_data = IssueData(
            created_by=self.user3,
            summary="Test Issue 3",
            project=self.project3,
            reporter=self.user3
            )
        issue3_data.save()
        issue3 = Issue(
            created_by=self.user3,
            current=issue3_data,
            sequence=Issue.objects.get_next_sequence_number(self.project3.id)
        )
        issue3.save()

        user1_issues = self.user1.list_issues()
        user2_issues = self.user2.list_issues()
        user3_issues = self.user3.list_issues()

        self.assertIn(issue1, user1_issues)
        self.assertNotIn(issue1, user2_issues)
        self.assertNotIn(issue1, user3_issues)
        self.assertIn(issue2, user1_issues)
        self.assertIn(issue2, user2_issues)
        self.assertNotIn(issue2, user3_issues)
        self.assertIn(issue3, user1_issues)
        self.assertNotIn(issue3, user2_issues)
        self.assertIn(issue3, user3_issues)

    def test_list_organizations(self):
        user1_organizations = self.user1.list_organizations()
        user2_organizations = self.user2.list_organizations()
        user3_organizations = self.user3.list_organizations()

        self.assertEqual(len(user1_organizations), 3)
        self.assertEqual(len(user2_organizations), 1)
        self.assertEqual(len(user3_organizations), 1)
        self.assertIn(self.organization1, user1_organizations)
        self.assertIn(self.organization2, user1_organizations)
        self.assertIn(self.organization3, user1_organizations)
        self.assertIn(self.organization2, user2_organizations)
        self.assertIn(self.organization3, user3_organizations)

    def test_list_users(self):
        user1_users = self.user1.list_users()
        user2_users = self.user2.list_users()
        user3_users = self.user3.list_users()

        self.assertEqual(len(user1_users), 3)
        self.assertIn(self.user1, user1_users)
        self.assertIn(self.user2, user1_users)
        self.assertIn(self.user3, user1_users)
        self.assertEqual(len(user2_users), 2)
        self.assertIn(self.user1, user2_users)
        self.assertIn(self.user2, user2_users)
        self.assertNotIn(self.user3, user2_users)
        self.assertEqual(len(user3_users), 2)
        self.assertIn(self.user1, user3_users)
        self.assertNotIn(self.user2, user3_users)
        self.assertIn(self.user3, user3_users)
