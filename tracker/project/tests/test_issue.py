from django.test import TestCase
from django.utils import timezone

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from project.models.issue_type import BuiltInIssueType
from project.models.priority import BuiltInIssuePriority
from project.models.status import BuiltInIssueStatus
from project.models.severity import BuiltInIssueSeverity
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData
from project.models.issue import Issue


class IssueActiveManagerTests(TestCase):
    def setUp(self):
        """
        Creates 3 users, 3 organizatios, 3 projects, and 1 git repository.
        User1 is in all 3 organizations explicitly, projects 1 and 2 explicitly as a user, and project 3 by being in the organization, and owns the git repository.
        User2 is in organization 2 and project 2 explictly.
        User3 is in organization 3.
        """

        BuiltInIssueType.objects.initialize_built_in_issue_types()
        BuiltInIssuePriority.objects.initialize_built_in_issue_priorities()
        BuiltInIssueStatus.objects.initialize_built_in_issue_statuses()
        BuiltInIssueSeverity.objects.initialize_built_in_issue_severities()

        self.system_user = CoreUser.objects.get_or_create_system_user()

        self.user1 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        self.user2 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser2@project-tracker.dev', 'password': 'password'})
        self.user3 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser3@project-tracker.dev', 'password': 'password'})

        self.organization1_data = OrganizationData.objects.create(
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
        self.organization1 = Organization.objects.create(
            created_by_id=self.user1.id,
            current=self.organization1_data,
            )
        self.organization1_data.organization = self.organization1
        self.organization1_data.save()
        self.organization1.members.add(self.user1)

        self.organization2_data = OrganizationData.objects.create(
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
        self.organization2 = Organization.objects.create(
            created_by_id=self.user2.id,
            current=self.organization2_data,
            )
        self.organization2_data.organization = self.organization2
        self.organization2_data.save()
        self.organization2.members.add(self.user1, self.user2)

        self.organization3_data = OrganizationData.objects.create(
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
        self.organization3 = Organization.objects.create(
            created_by_id=self.user3.id,
            current=self.organization3_data,
            )
        self.organization3_data.organization = self.organization3
        self.organization3_data.save()
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
        self.git_repository1_data.git_repository = self.git_repository1
        self.git_repository1_data.save()

        self.project1_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project 1",
            description="Initial Project 1 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data)
        self.project1_data.project = self.project1
        self.project1_data.save()
        self.project1_label_data = ProjectLabelData.objects.create(
            created_by=self.user1,
            label='project01',
            description='Project 01 Label'
        )
        self.project1_label = ProjectLabel.objects.create(
            created_by=self.user1,
            current=self.project1_label_data,
            project=self.project1
        )
        self.project1_label_data.project_label = self.project1_label
        self.project1_label_data.save()
        self.project1.label = self.project1_label
        self.project1.git_repositories.add(self.git_repository1)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.project2_data = ProjectData.objects.create(
            created_by=self.user2,
            name="Initial Project 2",
            description="Initial Project 2 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project2 = Project.objects.create(created_by=self.user2, current=self.project2_data)
        self.project2_data.project = self.project2
        self.project2_data.save()
        self.project2.users.add(self.user1, self.user2)

        self.project3_data = ProjectData.objects.create(
            created_by=self.system_user,
            name="initialproject3",
            description="Initial Project 3 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project3 = Project.objects.create(created_by=self.system_user, current=self.project3_data)
        self.project3_data.project = self.project3
        self.project3_data.save()
        self.organization3.projects.add(self.project3.id)

        self.organization1_data.refresh_from_db()
        self.organization1.refresh_from_db()
        self.organization2_data.refresh_from_db()
        self.organization2.refresh_from_db()
        self.organization3_data.refresh_from_db()
        self.organization3.refresh_from_db()
        self.git_repository1_data.refresh_from_db()
        self.git_repository1.refresh_from_db()
        self.project1_data.refresh_from_db()
        self.project1.refresh_from_db()
        self.project1_label.refresh_from_db()
        self.project1_label_data.refresh_from_db()
        self.project2_data.refresh_from_db()
        self.project2.refresh_from_db()
        self.project3_data.refresh_from_db()
        self.project3.refresh_from_db()

    def test_list_built_in_types(self):
        built_in_types = Issue.objects.list_built_in_types()
        self.assertGreater(len(built_in_types), 1)
        built_in_types = Issue.active_objects.list_built_in_types()
        self.assertGreater(len(built_in_types), 1)

    def test_list_built_in_priorities(self):
        built_in_priorities = Issue.objects.list_built_in_priorities()
        self.assertGreater(len(built_in_priorities), 1)
        built_in_priorities = Issue.active_objects.list_built_in_priorities()
        self.assertGreater(len(built_in_priorities), 1)

    def test_list_built_in_statuses(self):
        built_in_statuses = Issue.objects.list_built_in_statuses()
        self.assertGreater(len(built_in_statuses), 1)
        built_in_statuses = Issue.active_objects.list_built_in_statuses()
        self.assertGreater(len(built_in_statuses), 1)

    def test_list_built_in_severities(self):
        built_in_severities = Issue.objects.list_built_in_severities()
        self.assertGreater(len(built_in_severities), 1)
        built_in_severities = Issue.active_objects.list_built_in_severities()
        self.assertGreater(len(built_in_severities), 1)

    def test_list_versions(self):
        versions = Issue.objects.list_versions(self.project1.id)
        self.assertEqual(len(versions), 0)
        versions = Issue.active_objects.list_versions(self.project1.id)
        self.assertEqual(len(versions), 0)

    def test_list_components(self):
        components = Issue.objects.list_components(self.project1.id)
        self.assertEqual(len(components), 0)
        components = Issue.active_objects.list_components(self.project1.id)
        self.assertEqual(len(components), 0)
