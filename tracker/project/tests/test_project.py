from django.test import TestCase
from django.utils import timezone

from project.models.project import Project, ProjectData
from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models import issue as issue_models


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user1 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        self.user2 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser2@project-tracker.dev', 'password': 'password'})
        self.user3 = CoreUser.objects.create_core_user_from_web(
            {'email': 'testuser3@project-tracker.dev', 'password': 'password'})

        self.project1_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project 1",
            description="Initial Description 1",
            start_date=timezone.now(),
            is_active=True
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data)
        self.project1.update_project_data(user_id=self.user1.id, project_data={
            'users': [self.user1.id, self.user2.id, self.user3.id]})

        self.project2_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project 2",
            description="Initial Description 2",
            start_date=timezone.now(),
            is_active=True
            )
        self.project2 = Project.objects.create(created_by=self.user2, current=self.project2_data)
        self.project2.update_project_data(user_id=self.user2.id, project_data={
            'users': [self.user2.id, self.user3.id]})

        self.git_repository_data = GitRepositoryData.objects.create(
            created_by=self.user1,
            name="Initial Repo",
            description="Initial Repo Description",
            url="https://github.com/example/repo"
            )
        self.git_repository = GitRepository.objects.create(
            created_by=self.user1, current=self.git_repository_data)

        self.project1.current.git_repositories.add(self.git_repository)
        self.project1.current.users.add(self.user1)
        self.project1.current.users.add(self.user2)
        self.project1.current.save()

        self.project2.current.users.add(self.user2)
        self.project2.current.save()

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
        self.project1.update_project_data(user_id=self.user1.id, project_data=new_data)
        self.project1.refresh_from_db()

        self.assertEqual(self.project1.current.name, 'Updated Project with Label')
        self.assertEqual(self.project1.current.label.current.label, 'new-project-label')
        self.assertEqual(self.project1.current.label.current.description,
                         'New Project Label Description')
        self.assertEqual(self.project1.current.label.current.color, '#123456')

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
            'name': 'Updated Project with M2M',
            'git_repositories': [self.git_repository.id, new_repo.id],
            'users': [self.user1.id, new_user.id]
            }
        self.project1.update_project_data(user_id=self.user1.id, project_data=new_data)
        self.project1.refresh_from_db()

        self.assertEqual(self.project1.current.name, 'Updated Project with M2M')
        self.assertIn(new_repo, self.project1.current.git_repositories.all())
        self.assertIn(new_user, self.project1.current.users.all())

    def test_list_project_users(self):
        users = self.project1.list_users(self.user1)
        user_ids = users.values_list('id', flat=True)

        self.assertIn(self.user1.id, user_ids)
        self.assertIn(self.user2.id, user_ids)
        self.assertIn(self.user3.id, user_ids)
        self.assertEqual(users.count(), 3)

    def test_list_project_issues(self):
        issue_data1 = issue_models.IssueData.objects.create(
            created_by=self.user1,
            reporter=self.user1,
            summary="Issue 1",
            description="Description for issue 1",
            project=self.project1
            )
        issue1 = issue_models.Issue.objects.create(
            created_by=self.user1,
            sequence=1,
            current=issue_data1
            )
        issue_data2 = issue_models.IssueData.objects.create(
            created_by=self.user1,
            reporter=self.user1,
            summary="Issue 2",
            description="Description for issue 2",
            project=self.project1
            )
        issue2 = issue_models.Issue.objects.create(
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
        issue_data1 = issue_models.IssueData.objects.create(
            created_by=self.user1,
            reporter=self.user1,
            summary="Issue 1",
            description="Description for issue 1",
            project=self.project1
            )
        issue1 = issue_models.Issue.objects.create(
            created_by=self.user1,
            sequence=1,
            current=issue_data1
            )
        issue_data2 = issue_models.IssueData.objects.create(
            created_by=self.user2,
            reporter=self.user2,
            summary="Issue 2",
            description="Description for issue 2",
            project=self.project2
            )
        issue2 = issue_models.Issue.objects.create(
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
