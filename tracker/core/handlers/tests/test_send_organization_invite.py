from unittest import mock

from django.test import TestCase

from core.tasks.send_organization_invite import send_organization_invite_email


class TestSendOrganizationInviteView(TestCase):
    def test_send_organization_invite_view_get(self):
        with mock.patch('django.core.mail.EmailMultiAlternatives.send') as mock_send_mail:
            send_organization_invite_email('test_user_2@project-tracker.dev', 'Test Organization', 'https://project-tracker.dev/accept_invite/12345')
            mock_send_mail.assert_called_once()
