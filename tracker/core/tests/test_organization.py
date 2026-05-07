from django.test import TestCase
from django.utils import timezone

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from subscription.models.organization import OrganizationSubscriptionType, OrganizationSubscription, OrganizationSubscriptionData
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.project import Project, ProjectData


class UpdateOrganizationDataTest(TestCase):
    def setUp(self):
        OrganizationSubscriptionType.objects.initialize_subscriptions()
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
            subscription=OrganizationSubscription.active_objects.first(),
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

        self.organization.git_repositories.add(self.git_repo1)
        self.organization.members.add(self.member1)
        self.organization.projects.add(self.project1)
        self.organization.save()

    def test_update_organization_data(self):
        new_organization_data = {
            'name': 'Updated Organization Name',
            'description': 'Updated Description',
            }

        self.organization.update_organization_data(self.member1.id, new_organization_data)
        self.organization.refresh_from_db()

        self.assertEqual(self.organization.current.name, 'Updated Organization Name')
        self.assertEqual(self.organization.current.description, 'Updated Description')

    def test_update_organization_users(self):
        new_members = [str(self.member1.id), str(self.member2.id)]

        self.organization.update_members(new_members)
        self.organization.refresh_from_db()

        self.assertEqual(self.organization.current.name, 'Test Organization')
        self.assertEqual(self.organization.members.count(), 2)
        self.assertTrue(self.organization.members.filter(id=self.member1.id).exists())
        self.assertTrue(self.organization.members.filter(id=self.member2.id).exists())

    def test_get_subscription(self):
        subscription = self.organization.get_subscription()
        self.assertIsNone(subscription)
        subscription_data = OrganizationSubscriptionData.objects.create(created_by=self.member1, subscription_type=OrganizationSubscriptionType.active_objects.get(current__name='Trial'), expiration_date=timezone.now() + timezone.timedelta(days=7), expired=False)
        self.organization.subscription = OrganizationSubscription.objects.create(created_by=self.member1, org=self.organization, current=subscription_data)
        self.organization.save()
        subscription = self.organization.get_subscription()
        self.assertEqual(subscription, OrganizationSubscription.active_objects.first())
