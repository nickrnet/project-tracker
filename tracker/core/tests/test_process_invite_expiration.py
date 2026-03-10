import logging

from django.test import TestCase
from django.utils import timezone

from core.models.user import CoreUser
from core.models.organization import Organization, OrganizationData
from core.models.organization_invites import OrganizationInvite, OrganizationInviteData
from core.tasks import process_invite_expiration
from project.models.project import Project, ProjectData


class TestProcessInviteExpiration(TestCase):
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
        self.organization_data = OrganizationData.objects.create(**organization_data)
        self.organization = Organization.objects.create(
            created_by_id=self.member1.id,
            current=self.organization_data,
            )
        project_data1 = {
            'created_by_id': str(self.member1.id),
            'name': 'Project 1',
            'is_active': True,
            }
        self.project_data1 = ProjectData.objects.create(**project_data1)
        self.project1 = Project.objects.create(
            created_by_id=self.member1.id,
            current=self.project_data1,
            )
        self.organization.members.add(self.member1)
        self.organization.projects.add(self.project1)
        self.organization.save()

    def test_process_invite_expiration_does_not_expire_valid_invites(self):
        # create an invite for member2
        invite_data1 = {
            'created_by_id': str(self.member1.id),
            'email': 'testuser2@project-tracker.dev',
            'invited_by_id': str(self.member1.id),
            'organization_id': str(self.organization.id),
            'status': 'PENDING',
            'expires_on': timezone.now() + timezone.timedelta(days=1),
            }
        self.invite_data1 = OrganizationInviteData.objects.create(**invite_data1)
        self.invite1 = OrganizationInvite.objects.create(
            created_by_id=self.member1.id,
            current=self.invite_data1,
            )
        with self.assertLogs(logger=logging.getLogger('core.tasks.process_invite_expiration'), level='INFO') as cm:
            process_invite_expiration.process_organization_invite_expiration()
        self.assertIn("No invites to expire.", cm.output[1])
        self.invite1.refresh_from_db()
        self.assertEqual(self.invite1.current.status, 'PENDING')

    def test_process_invite_expiration_expires_invites(self):
        # create an expired invite for member2
        invite_data2 = {
            'created_by_id': str(self.member1.id),
            'email': 'testuser2@project-tracker.dev',
            'invited_by_id': str(self.member1.id),
            'organization_id': str(self.organization.id),
            'status': 'PENDING',
            'expires_on': timezone.now() - timezone.timedelta(days=1),
            }
        self.invite_data2 = OrganizationInviteData.objects.create(**invite_data2)
        self.invite2 = OrganizationInvite.objects.create(
            created_by_id=self.member1.id,
            current=self.invite_data2,
            )
        with self.assertLogs(logger=logging.getLogger('core.tasks.process_invite_expiration'), level='INFO') as cm:
            process_invite_expiration.process_organization_invite_expiration()
        self.assertIn("Expired 1 organization invites.", cm.output[1])
        self.invite2.refresh_from_db()
        self.assertEqual(self.invite2.current.status, 'EXPIRED')
