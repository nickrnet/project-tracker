import uuid

from django.test import TestCase

from project.models.issue_type import BuiltInIssueType


class TestBuiltInIssueTypeActiveManager(TestCase):
    def setUp(self):
        BuiltInIssueType.objects.initialize_built_in_issue_types()

    def test_built_in_issue_type_initializer(self):
        built_in_types = [
            ('c166c9dc-f058-4fb7-99c3-eb2bc14a46ee', 'CHANGE_REQUEST', 'Change Request'),
            ('94e3841b-3c88-4273-9dd0-190aa5e7c8ea', 'PROBLEM', 'Problem'),
            ('d34e6879-e36c-4eb4-a9e5-b74800cebbed', 'INCIDENT', 'Incident'),
            ('b7c197df-723d-4687-b421-327b6fc2fcf8', 'SERVICE_REQUEST', 'Service Request'),
            ('849a2e5a-9920-47f8-8545-2546645995da', 'TEST', 'Test'),
            ('f83fe0be-6c55-47a4-b3e7-025db8e0c63d', 'IMPROVEMENT', 'Improvement'),
            ('218ffda9-4e5d-48a9-b90e-46ae759d80a3', 'ENHANCEMENT', 'Enhancement'),
            ('6d8e2776-ad44-41e1-bca6-6637cdeb70e6', 'QUESTION', 'Question'),
            ('a9198bed-0f07-4482-9687-6465d73a6910', 'PROPOSAL', 'Proposal'),
            ('ee0e2c17-99c2-40fb-ad28-1c23773d7d42', 'SPIKE', 'Spike'),
            ('00305b27-674b-469a-85b9-8a0b8cb63597', 'SUB_TASK', 'Sub-task'),
            ('c5da1c3c-ffa1-47fb-adbf-087a9d3527f9', 'TASK', 'Task'),
            ('33b0397f-3da9-4a91-ae48-5aa30d71dfe6', 'FEATURE', 'Feature'),
            ('bc3b8be9-0093-4826-80ba-e9874e8c05ca', 'STORY', 'Story'),
            ('8b4ba108-33b0-4481-bf52-ad891c7d9226', 'EPIC', 'Epic'),
            ('d43acc25-927a-4666-865f-2dd93b8418cb', 'DOCUMENTATION', 'Documentation'),
            ('b9a4b28c-b52d-42be-ad70-79f0e94fa462', 'BUG', 'Bug'),
            ]
        installed_issue_type_ids = BuiltInIssueType.objects.all().values_list('id', flat=True)
        self.assertEqual(BuiltInIssueType.active_objects.count(), 17)
        for id, type, description in built_in_types:
            self.assertIn(uuid.UUID(id), installed_issue_type_ids)

        # Rerun initializer
        BuiltInIssueType.objects.initialize_built_in_issue_types()

        # Make sure BuiltInIssueType is not duplicated
        installed_issue_type_ids = BuiltInIssueType.objects.all().values_list('id', flat=True)
        self.assertEqual(BuiltInIssueType.active_objects.count(), 17)
        for id, type, description in built_in_types:
            self.assertIn(uuid.UUID(id), installed_issue_type_ids)
