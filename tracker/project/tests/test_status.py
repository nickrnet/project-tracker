import uuid

from django.test import TestCase

from project.models.status import BuiltInIssueStatus


class TestBuiltInIssueStatusActiveManager(TestCase):
    def setUp(self):
        BuiltInIssueStatus.objects.initialize_built_in_issue_statuses()

    def test_built_in_issue_status_initializer(self):
        self.assertEqual(BuiltInIssueStatus.active_objects.count(), 7)
        self.assertIn(uuid.UUID('24c03dc0-a98f-4125-a9db-51781e610444'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('24494695-c0f8-4a90-aacc-670776b40ff9'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('bef3f9f1-0f37-41be-b405-322731c76b16'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('332f5852-a6e1-415f-bef5-44fcd36dbfc9'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('4c509937-972d-470c-9589-362ba90c1268'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('86780f1e-e3a8-4869-bc6b-1e9a3111ef9f'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('34d28f8e-dd1c-4871-938b-3ed56f960093'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))

        # Rerun initializer
        BuiltInIssueStatus.objects.initialize_built_in_issue_statuses()

        # Make sure BuiltInIssueStatus is not duplicated
        self.assertEqual(BuiltInIssueStatus.active_objects.count(), 7)
        self.assertIn(uuid.UUID('24c03dc0-a98f-4125-a9db-51781e610444'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('24494695-c0f8-4a90-aacc-670776b40ff9'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('bef3f9f1-0f37-41be-b405-322731c76b16'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('332f5852-a6e1-415f-bef5-44fcd36dbfc9'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('4c509937-972d-470c-9589-362ba90c1268'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('86780f1e-e3a8-4869-bc6b-1e9a3111ef9f'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
        self.assertIn(uuid.UUID('34d28f8e-dd1c-4871-938b-3ed56f960093'), BuiltInIssueStatus.objects.all().values_list('id', flat=True))
