from django.test import TestCase
from django.utils import timezone

from core.models.user import CoreUser
from core.models.organization import Organization, OrganizationData
from core.models.organization_invites import OrganizationInvite, OrganizationInviteData
from project.models.project import Project, ProjectData


class TestOrganizationInvites(TestCase):
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

    def test_send_invite_email(self):
        invite_data = OrganizationInviteData.objects.create(
            created_by=self.member1,
            created_on=timezone.now(),
            email='testuser2@project-tracker.dev',
            invited_by=self.member1,
            organization=self.organization,
            status='PENDING',
            expires_on=timezone.now() + timezone.timedelta(days=7),
            )
        invite = OrganizationInvite.objects.create(
            created_by=self.member1,
            created_on=timezone.now(),
            current=invite_data,
            )
        self.organization.member_invites.add(invite)
        self.organization.save()

        accept_organization_invite_url = f"/accept_organization_invite/{invite.id}/"
        invite.send_invite_email(accept_organization_invite_url)
