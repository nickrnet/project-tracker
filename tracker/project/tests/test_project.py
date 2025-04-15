from django.test import TestCase
from django.utils import timezone

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData
from project.models.issue import Issue, IssueData


class ProjectModelTest(TestCase):
    def setUp(self):
        """
        Creates 3 users, 3 organizatios, 3 projects, and 1 git repository.
        User1 is in all 3 organizations explicitly, projects 1 and 2 explicitly as a user, and project 3 by being in the organization, and owns the git repository.
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
            label=self.project1_data_label,
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
            name="initialproject3",
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
        
    def test_generate_project_label_string(self):
        project_label_str = self.project2.current.generate_label()
        self.assertEqual(project_label_str, 'initial-project-2')
        project_label_str = self.project3.current.generate_label()
        self.assertEqual(project_label_str, 'initialproject3')

    def test_update_project_data(self):
        new_data = {
            'name': 'Updated Project',
            'description': 'Updated Description',
            'is_active': False
            }
        self.project1.update_project_data(user_id=self.user1.id, project_data=new_data)
        self.project1.refresh_from_db()

        self.assertEqual(self.project1.current.name, 'Updated Project')
        self.assertEqual(self.project1.current.description, 'Updated Description')
        self.assertFalse(self.project1.current.is_active)

    def test_update_project_data_with_label(self):
        new_label_data = {
            'current': {
                'label': 'new-project-label',
                'description': 'New Project Label Description',
                'color': '#123456'
                }
            }
        new_data = {
            'name': 'Updated Project with Label',
            'label': new_label_data
            }
        # Update a project that already has a label
        self.project1.update_project_data(user_id=self.user1.id, project_data=new_data.copy())
        self.project1.refresh_from_db()

        self.assertEqual(self.project1.current.name, 'Updated Project with Label')
        self.assertEqual(self.project1.current.label.current.label, 'new-project-label')
        self.assertEqual(self.project1.current.label.current.description,
                         'New Project Label Description')
        self.assertEqual(self.project1.current.label.current.color, '#123456')
        
        # Update a project that does not have a label
        self.project2.update_project_data(user_id=self.user2.id, project_data=new_data.copy())
        self.project2.refresh_from_db()

        self.assertEqual(self.project2.current.name, 'Updated Project with Label')
        self.assertEqual(self.project2.current.label.current.label, 'new-project-label')
        self.assertEqual(self.project2.current.label.current.description,
                         'New Project Label Description')
        self.assertEqual(self.project2.current.label.current.color, '#123456')

    def test_update_project_data_with_git_repositories_and_users(self):
        new_user = CoreUser.objects.create_core_user_from_web(
            {'email': 'newuser@project-tracker.dev', 'password': 'password'})
        new_repo_data = GitRepositoryData.objects.create(
            created_by=self.user1,
            name="New Repo",
            description="New Repo Description",
            url="https://github.com/example/newrepo"
            )
        new_repo = GitRepository.objects.create(created_by=self.user1, current=new_repo_data)
        new_data = {
            'name': 'Updated Project with Git Repositories and Users',
            'git_repositories': [self.git_repository1.id, new_repo.id],
            'users': [self.user1.id, new_user.id]
            }
        self.project1.update_project_data(user_id=self.user1.id, project_data=new_data)
        self.project1.refresh_from_db()

        self.assertEqual(self.project1.current.name, 'Updated Project with Git Repositories and Users')
        self.assertIn(new_repo, self.project1.current.git_repositories.all())
        self.assertIn(new_user, self.project1.current.users.all())
        
        # Test removing things
        new_data = {
            'git_repositories': [self.git_repository1.id],
            'users': [self.user1.id]
            }
        self.project1.update_project_data(user_id=self.user1.id, project_data=new_data)
        self.project1.refresh_from_db()

        self.assertEqual(self.project1.current.name, 'Updated Project with Git Repositories and Users')
        self.assertIn(self.git_repository1, self.project1.current.git_repositories.all())
        self.assertNotIn(new_repo, self.project1.current.git_repositories.all())
        self.assertIn(self.user1, self.project1.current.users.all())
        self.assertNotIn(new_user, self.project1.current.users.all())

    def test_list_project_users(self):
        project1_user_ids = self.project1.list_users().values_list('id', flat=True)
        project2_user_ids = self.project2.list_users().values_list('id', flat=True)
        project3_user_ids = self.project3.list_users().values_list('id', flat=True)
        
        self.assertEqual(project1_user_ids.count(), 1)
        self.assertIn(self.user1.id, project1_user_ids)
        self.assertNotIn(self.user2.id, project1_user_ids)
        self.assertNotIn(self.user3.id, project1_user_ids)

        self.assertEqual(project2_user_ids.count(), 2)
        self.assertIn(self.user1.id, project2_user_ids)
        self.assertIn(self.user2.id, project2_user_ids)
        self.assertNotIn(self.user3.id, project2_user_ids)

        self.assertEqual(project3_user_ids.count(), 2)
        self.assertIn(self.user1.id, project3_user_ids)
        self.assertNotIn(self.user2.id, project3_user_ids)
        self.assertIn(self.user3.id, project3_user_ids)

    def test_list_project_issues(self):
        issue_data1 = IssueData.objects.create(
            created_by=self.user1,
            reporter=self.user1,
            summary="Issue 1",
            description="Description for issue 1",
            project=self.project1
            )
        issue1 = Issue.objects.create(
            created_by=self.user1,
            sequence=1,
            current=issue_data1
            )
        issue_data2 = IssueData.objects.create(
            created_by=self.user1,
            reporter=self.user1,
            summary="Issue 2",
            description="Description for issue 2",
            project=self.project1
            )
        issue2 = Issue.objects.create(
            created_by=self.user1,
            sequence=2,
            current=issue_data2
            )

        issues = self.project1.list_issues()
        issue_ids = issues.values_list('id', flat=True)

        self.assertIn(issue1.id, issue_ids)
        self.assertIn(issue2.id, issue_ids)
        self.assertEqual(issues.count(), 2)

    def test_list_issues_in_projects(self):
        issue_data1 = IssueData.objects.create(
            created_by=self.user1,
            reporter=self.user1,
            summary="Issue 1",
            description="Description for issue 1",
            project=self.project1
            )
        issue1 = Issue.objects.create(
            created_by=self.user1,
            sequence=1,
            current=issue_data1
            )
        issue_data2 = IssueData.objects.create(
            created_by=self.user2,
            reporter=self.user2,
            summary="Issue 2",
            description="Description for issue 2",
            project=self.project2
            )
        issue2 = Issue.objects.create(
            created_by=self.user1,
            sequence=2,
            current=issue_data2
            )

        project1_issues = self.project1.list_issues()
        project1_issue_ids = project1_issues.values_list('id', flat=True)
        project2_issues = self.project2.list_issues()
        project2_issue_ids = project2_issues.values_list('id', flat=True)

        self.assertEqual(project1_issues.count(), 1)
        self.assertEqual(project2_issues.count(), 1)
        self.assertIn(issue1.id, project1_issue_ids)
        self.assertNotIn(issue1.id, project2_issue_ids)
        self.assertIn(issue2.id, project2_issue_ids)
        self.assertNotIn(issue2.id, project1_issue_ids)
