from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models.user import CoreUser
from core.models.organization import Organization, OrganizationData
from core.models.organization_invites import OrganizationInvite, OrganizationInviteData
from project.models.project import Project, ProjectData


class TestOrganizationAcceptInviteView(TestCase):
    def setUp(self):
        self.member1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password'})
        self.member2 = CoreUser.objects.create_core_user_from_web({'email': 'testuser2@project-tracker.dev', 'password': 'password'})
        self.member3 = CoreUser.objects.create_core_user_from_web({'email': 'testuser3@project-tracker.dev', 'password': 'password'})
        organization_data = {
            'created_by_id': str(self.member1.id),
            'name': 'Test Organization',
            'responsible_party_email': 'testuser1@project-tracker.dev',
            'responsible_party_phone': '123-456-7890',
            'address_line_1': '123 Main St',
            'city': 'Anytown',
            'state': 'NY',
            'postal_code': '12345',
            }
        self.organization_data = OrganizationData.objects.create(**organization_data)
        self.organization = Organization.objects.create(
            created_by_id=self.member1.id,
            current=self.organization_data,
            )
        organization2_data = {
            'created_by_id': str(self.member1.id),
            'name': 'Test Organization',
            'responsible_party_email': 'testuser1@project-tracker.dev',
            'responsible_party_phone': '123-456-7890',
            'address_line_1': '123 Main St',
            'city': 'Anytown',
            'state': 'NY',
            'postal_code': '12345',
            }
        self.organization2_data = OrganizationData.objects.create(**organization2_data)
        self.organization2 = Organization.objects.create(
            created_by_id=self.member2.id,
            current=self.organization2_data,
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
        self.organization2.members.add(self.member2)
        self.invite_data = OrganizationInviteData.objects.create(
            created_by=self.member1,
            created_on=timezone.now(),
            email='testuser2@project-tracker.dev',
            invited_by=self.member1,
            organization=self.organization,
            status='PENDING',
            expires_on=timezone.now() + timezone.timedelta(days=7),
            )
        self.invite = OrganizationInvite.objects.create(
            created_by=self.member1,
            created_on=timezone.now(),
            current=self.invite_data,
            )
        self.organization.member_invites.add(self.invite)
        self.organization.save()
        self.invite2_data = OrganizationInviteData.objects.create(
            created_by=self.member2,
            created_on=timezone.now(),
            email='testuser3@project-tracker.dev',
            invited_by=self.member2,
            organization=self.organization2,
            status='PENDING',
            expires_on=timezone.now() + timezone.timedelta(days=7),
            )
        self.invite2 = OrganizationInvite.objects.create(
            created_by=self.member2,
            created_on=timezone.now(),
            current=self.invite2_data,
            )
        self.organization2.member_invites.add(self.invite2)
        self.organization2.save()

    def test_organization_accept_invite_view_get(self):
        self.client.force_login(user=self.member2.user)
        response = self.client.get(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/organization/accept_organization_invite.html')

    def test_organization_accept_invite_view_get_not_logged_in(self):
        response = self.client.get(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite.id)}))
        self.assertRedirects(response, '/login?next=/organization/' + str(self.organization.id) + '/accept_organization_invite/' + str(self.invite.id) + '/')

    def test_organization_accept_invite_view_get_invalid_invite_when_logged_in(self):
        self.client.force_login(user=self.member2.user)
        response = self.client.get(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': '4b3117ea-d53c-456a-a0e3-b36b0c298224'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('The specified invite is invalid.', str(messages))

    def test_organization_accept_invite_view_get_invalid_invite_when_not_logged_in(self):
        response = self.client.get(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': '4b3117ea-d53c-456a-a0e3-b36b0c298224'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/organization/' + str(self.organization.id) + '/accept_organization_invite/4b3117ea-d53c-456a-a0e3-b36b0c298224/')

    def test_organization_accept_invite_view_get_logged_in_user_was_not_recipient(self):
        self.client.force_login(user=self.member3.user)
        response = self.client.get(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('The specified invite is invalid.', str(messages))

    def test_organization_accept_invite_view_get_expired_invite_when_logged_in(self):
        self.invite.current.status = 'EXPIRED'
        self.invite.current.save()
        self.client.force_login(user=self.member2.user)
        response = self.client.get(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('The specified invite is invalid.', str(messages))

    def test_organization_accept_invite_view_get_expired_invite_when_not_logged_in(self):
        self.invite.current.status = 'EXPIRED'
        self.invite.current.save()
        response = self.client.get(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/organization/' + str(self.organization.id) + '/accept_organization_invite/' + str(self.invite.id) + '/')

    def test_organization_accept_invite_view_post(self):
        self.client.force_login(user=self.member2.user)
        response = self.client.post(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite.id)}), {'response': 'accepted'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(f'You have successfully joined the organization {self.organization.current.name}.', str(messages))
        self.invite.refresh_from_db()
        self.invite.current.refresh_from_db()
        self.assertEqual(self.invite.current.status, 'ACCEPTED')
        self.organization.refresh_from_db()
        self.assertIn(self.member2, self.organization.members.all())

    def test_organization_accept_invite_view_post_invite_does_not_exist(self):
        self.client.force_login(user=self.member2.user)
        response = self.client.post(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': '207b815c-3e78-4d45-9a02-2f04d0a9195f'}), {'response': 'accepted'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('The specified invite is invalid.', str(messages))
        self.invite.refresh_from_db()
        self.invite.current.refresh_from_db()
        self.assertEqual(self.invite.current.status, 'PENDING')
        self.organization.refresh_from_db()
        self.assertNotIn(self.member2, self.organization.members.all())

    def test_organization_accept_invite_view_post_decline(self):
        self.client.force_login(user=self.member2.user)
        response = self.client.post(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite.id)}), {'response': 'declined'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')
        self.assertIn("You have declined the organization invite.", str(messages))
        self.invite.refresh_from_db()
        self.invite.current.refresh_from_db()
        self.assertEqual(self.invite.current.status, 'DECLINED')
        self.organization.refresh_from_db()
        self.assertNotIn(self.member2, self.organization.members.all())

    def test_organization_accept_invite_view_post_accept_different_organization_invite(self):
        self.client.force_login(user=self.member3.user)
        response = self.client.post(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite2.id)}), {'response': 'accepted'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/organizations')
        self.invite.refresh_from_db()
        self.invite.current.refresh_from_db()
        self.organization.refresh_from_db()
        self.assertIn("The specified invite is invalid.", str(messages))
        self.assertEqual(self.invite.current.status, 'PENDING')
        self.assertIn(self.member1, self.organization.members.all())

    def test_organization_accept_invite_view_post_accept_already_in_organization(self):
        self.invite.current.email = self.member1.user.email
        self.invite.current.save()
        self.client.force_login(user=self.member1.user)
        response = self.client.post(reverse('accept_organization_invite', kwargs={'organization_id': str(self.organization.id), 'invite_id': str(self.invite.id)}), {'response': 'accepted'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')
        self.invite.refresh_from_db()
        self.invite.current.refresh_from_db()
        self.organization.refresh_from_db()
        self.assertIn("You are already a member of this organization.", str(messages))
        self.assertEqual(self.invite.current.status, 'PENDING')
        self.assertIn(self.member1, self.organization.members.all())
