from django.test import TestCase
from django.utils import timezone

from project.models.project import Project, ProjectData
from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData


class CoreUserTestCase(TestCase):
    def setUp(self):
        """
        Creates 3 users, 3 organizatios, 2 projects, and 1 git repository.
        User1 is in all 3 organizations explicitly, projects 1 and 2 explicitly as a user, and project 3 as being in the organization, and owns the git repository.
        User2 is in organization 2 and project 2 explictly.
        User3 is in organization 3.
        """

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
        self.organization1_data.members.add(self.user1)
        self.organization1_data.save()
        self.organization1 = Organization(
            created_by_id=self.user1.id,
            current=self.organization1_data,
            )
        self.organization1.save()

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
        self.organization2_data.members.add(self.user1, self.user2)
        self.organization2_data.save()
        self.organization2 = Organization(
            created_by_id=self.user2.id,
            current=self.organization2_data,
            )
        self.organization2.save()

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
        self.organization3_data.members.add(self.user1, self.user3)
        self.organization3_data.save()
        self.organization3 = Organization(
            created_by_id=self.user3.id,
            current=self.organization3_data,
            )
        self.organization3.save()

        self.git_repository1_data = GitRepositoryData.objects.create(
            created_by=self.user1,
            name="Initial Repo 1",
            description="Initial Repo 1 Description",
            url="https://github.com/example/repo1"
            )
        self.git_repository1_data.save()
        self.git_repository1 = GitRepository.objects.create(
            created_by=self.user1, current=self.git_repository1_data)

        self.project1_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project 1",
            description="Initial Project 1 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project1_data.save()
        self.project1_data.git_repositories.add(self.git_repository1)
        self.project1_data.users.add(self.user1)
        self.project1_data.save()
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data)

        self.project2_data = ProjectData.objects.create(
            created_by=self.user2,
            name="Initial Project 2",
            description="Initial Project 2 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project2_data.save()
        self.project2_data.users.add(self.user1, self.user2)
        self.project2_data.save()
        self.project2 = Project.objects.create(created_by=self.user2, current=self.project2_data)

        self.project3_data = ProjectData.objects.create(
            created_by=self.system_user,
            name="Initial Project 3",
            description="Initial Project 3 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project3_data.save()
        self.project3 = Project.objects.create(created_by=self.system_user, current=self.project3_data)

        self.organization3.update_organization_data(
            user_id=self.system_user.id,
            new_organization_data={
                'projects': [self.project3.id],
                }
            )

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
        pass

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
