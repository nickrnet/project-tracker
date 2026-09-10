from unittest import mock

from django.test import TestCase

from core.tasks.send_issue_update import send_issue_update_email


class TestSendIssueUpdate(TestCase):
    def test_send_issud_update(self):
        with mock.patch('django.core.mail.EmailMultiAlternatives.send') as mock_send_mail:
            send_issue_update_email('test_user_2@project-tracker.dev', 'TEST-PROJECT-1', 'https://project-tracker.dev/project/TEST-PROJECT/issue/3d1533bf-8690-470f-aff1-a4eb90e20cde')
            mock_send_mail.assert_called_once()
