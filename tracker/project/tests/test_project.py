from django.test import TestCase
from django.utils import timezone

from project.models.project import Project, ProjectData
from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        self.user2 = CoreUser.objects.create_core_user_from_web({'email': 'testuser2@project-tracker.dev', 'password': 'password'})
        self.user3 = CoreUser.objects.create_core_user_from_web({'email': 'testuser3@project-tracker.dev', 'password': 'password'})
        self.project_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project",
            description="Initial Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project = Project.objects.create(created_by=self.user1, current=self.project_data)
        self.project.update_project_data(user_id=self.user1.id, project_data={'users': [self.user1.id, self.user2.id, self.user3.id]})
        self.git_repository_data = GitRepositoryData.objects.create(
            created_by=self.user1,
            name="Initial Repo",
            description="Initial Repo Description",
            url="https://github.com/example/repo"
            )
        self.git_repository = GitRepository.objects.create(created_by=self.user1, current=self.git_repository_data)
        self.project.current.git_repositories.add(self.git_repository)
        self.project.current.users.add(self.user1)
        self.project.current.save()

    def test_update_project_data(self):
        new_data = {
            'name': 'Updated Project',
            'description': 'Updated Description',
            'is_active': False
            }
        self.project.update_project_data(user_id=self.user1.id, project_data=new_data)
        self.project.refresh_from_db()

        self.assertEqual(self.project.current.name, 'Updated Project')
        self.assertEqual(self.project.current.description, 'Updated Description')
        self.assertFalse(self.project.current.is_active)

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
        self.project.update_project_data(user_id=self.user1.id, project_data=new_data)
        self.project.refresh_from_db()

        self.assertEqual(self.project.current.name, 'Updated Project with Label')
        self.assertEqual(self.project.current.label.current.label, 'new-project-label')
        self.assertEqual(self.project.current.label.current.description, 'New Project Label Description')
        self.assertEqual(self.project.current.label.current.color, '#123456')

    def test_update_project_data_with_m2m_fields(self):
        new_user = CoreUser.objects.create_core_user_from_web({'email': 'newuser@project-tracker.dev', 'password': 'password'})
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
        self.project.update_project_data(user_id=self.user1.id, project_data=new_data)
        self.project.refresh_from_db()

        self.assertEqual(self.project.current.name, 'Updated Project with M2M')
        self.assertIn(new_repo, self.project.current.git_repositories.all())
        self.assertIn(new_user, self.project.current.users.all())

    def test_list_users(self):
        users = self.project.list_users(self.user1)
        user_ids = users.values_list('id', flat=True)

        self.assertIn(self.user1.id, user_ids)
        self.assertIn(self.user2.id, user_ids)
        self.assertIn(self.user3.id, user_ids)
        self.assertEqual(users.count(), 3)
