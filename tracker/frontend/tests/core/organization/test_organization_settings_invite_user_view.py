from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from core.models.user import CoreUser
from core.models.organization import Organization, OrganizationData
from core.models.organization_invites import OrganizationInvite
from project.models.project import Project, ProjectData


class TestOrganizationSettingsInviteUserView(TestCase):
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

    def test_organization_settings_invite_user_view_get(self):
        self.client.force_login(user=self.member1.user)
        response = self.client.get(reverse('organization_settings_invite_user', kwargs={'organization_id': str(self.organization.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_settings_invite_user_modal.html')

    def test_organization_settings_invite_user_view_get_organization_does_not_exist(self):
        self.client.force_login(user=self.member1.user)
        response = self.client.get(reverse('organization_settings_invite_user', kwargs={'organization_id': '5f2a1810-6d3d-43b1-8659-ef96e3c56e06'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('The specified organization does not exist. Create it and try again.', str(messages))

    def test_organization_settings_invite_user_view_get_user_not_in_organization(self):
        self.client.force_login(user=self.member2.user)
        response = self.client.get(reverse('organization_settings_invite_user', kwargs={'organization_id': str(self.organization.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('The specified organization does not exist. Create it and try again.', str(messages))

    def test_organization_settings_invite_user_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'email=' + self.member2.current.email
        self.client.force_login(user=self.member1.user)
        response = self.client.post(reverse('organization_settings_invite_user', kwargs={'organization_id': str(self.organization.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_invites_table.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(f'Invite sent to {self.member2.current.email}!', str(messages))
        self.organization.refresh_from_db()
        invite = OrganizationInvite.objects.get(current__email=self.member2.current.email)
        self.assertIn(invite, self.organization.member_invites.all())
        self.assertEqual(invite.current.status, 'PENDING')

    def test_organization_settings_invite_user_view_post_without_email_address(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'email='
        self.client.force_login(user=self.member1.user)
        response = self.client.post(reverse('organization_settings_invite_user', kwargs={'organization_id': str(self.organization.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_invites_table.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Email is required to send an invite.', str(messages))
        self.organization.refresh_from_db()
        with self.assertRaises(OrganizationInvite.DoesNotExist):
            OrganizationInvite.objects.get(current__email='')

    def test_organization_settings_invite_user_view_post_user_already_a_member(self):
        self.organization.members.add(self.member2)
        self.organization.save()
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'email=' + self.member2.current.email
        self.client.force_login(user=self.member1.user)
        response = self.client.post(reverse('organization_settings_invite_user', kwargs={'organization_id': str(self.organization.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/organization_invites_table.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('This user is already a member of your organization.', str(messages))
        self.organization.refresh_from_db()
        with self.assertRaises(OrganizationInvite.DoesNotExist):
            OrganizationInvite.objects.get(current__email=self.member2.current.email)
