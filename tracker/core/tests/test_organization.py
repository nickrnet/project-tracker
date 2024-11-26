from django.test import TestCase

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.project import Project, ProjectData


class UpdateOrganizationDataTest(TestCase):
    def setUp(self):
        self.member1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        self.member2 = CoreUser.objects.create_core_user_from_web({'email': 'testuser2@project-tracker.dev', 'password': 'password'})
        organization_data = {
            'created_by_id': str(self.member1.id),
            'name': 'Test Organization',
            'responsible_party_email': 'testuser1@project-tracker.dev',
            'responsible_party_phone': '123-456-7890',
            'address_line_1': '123 Main St',
            'city': 'Anytown',
            'state': 'NY',
            'postal_code': '12345',
            'is_paid': True,
            'number_users_allowed': 5,
            }
        git_repo_data1 = {
            'created_by_id': str(self.member1.id),
            'name': 'Repo 1'
            }
        git_repo_data2 = {
            'created_by_id': str(self.member2.id),
            'name': 'Repo 2'
            }
        project_data1 = {
            'created_by_id': str(self.member1.id),
            'name': 'Project 1',
            'is_active': True,
            }
        project_data2 = {
            'created_by_id': str(self.member2.id),
            'name': 'Project 2',
            'is_active': True,
            }
        self.organization_data = OrganizationData.objects.create(**organization_data)
        self.organization = Organization.objects.create(
            created_by_id=self.member1.id,
            current=self.organization_data,
            )
        self.git_repo_data1 = GitRepositoryData.objects.create(**git_repo_data1)
        self.git_repo1 = GitRepository.objects.create(
            created_by_id=self.member1.id,
            current=self.git_repo_data1,
            )
        self.git_repo_data2 = GitRepositoryData.objects.create(**git_repo_data2)
        self.git_repo2 = GitRepository.objects.create(
            created_by_id=self.member2.id,
            current=self.git_repo_data2,
            )
        self.project_data1 = ProjectData.objects.create(**project_data1)
        self.project1 = Project.objects.create(
            created_by_id=self.member1.id,
            current=self.project_data1,
            )
        self.project_data2 = ProjectData.objects.create(**project_data2)
        self.project2 = Project.objects.create(
            created_by_id=self.member1.id,
            current=self.project_data2,
            )

        self.organization.current.git_repositories.add(self.git_repo1)
        self.organization.current.members.add(self.member1)
        self.organization.current.projects.add(self.project1)
        self.organization.current.save()

    def test_update_organization_data(self):
        new_organization_data = {
            'name': 'Updated Organization Name',
            'description': 'Updated Description',
            'git_repositories': [self.git_repo1.id, self.git_repo2.id],
            'members': [self.member1.id, self.member2.id],
            'projects': [self.project1.id, self.project2.id]
            }

        self.organization.update_organization_data(self.member1.id, new_organization_data)
        self.organization.refresh_from_db()

        self.assertEqual(self.organization.current.name, 'Updated Organization Name')
        self.assertEqual(self.organization.current.description, 'Updated Description')
        self.assertEqual(self.organization.current.git_repositories.count(), 2)
        self.assertEqual(self.organization.current.members.count(), 2)
        self.assertEqual(self.organization.current.projects.count(), 2)
        self.assertIn(self.git_repo1, self.organization.current.git_repositories.all())
        self.assertIn(self.member1, self.organization.current.members.all())
        self.assertIn(self.project1, self.organization.current.projects.all())
        self.assertIn(self.git_repo2, self.organization.current.git_repositories.all())
        self.assertIn(self.member2, self.organization.current.members.all())
        self.assertIn(self.project2, self.organization.current.projects.all())
