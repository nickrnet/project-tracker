import uuid

from django.test import TestCase

from project.models.priority import BuiltInIssuePriority


class TestBuiltInIssuePriorityActiveManager(TestCase):
    def setUp(self):
        BuiltInIssuePriority.objects.initialize_built_in_issue_priorities()

    def test_built_in_issue_priority_initializer(self):
        built_in_priorities = [
            ('cbb014f3-f9ab-46da-926e-7d76bca69470', 'CRITICAL', 'Critical'),
            ('376295d8-2132-410f-a9aa-4e32757f5324', 'HIGH', 'High'),
            ('9756bb3a-521f-40a1-ae26-d1d2ecf2a54d', 'MEDIUM', 'Medium'),
            ('91dcbc0e-8189-4505-83e2-70892bb3bc26', 'LOW', 'Low'),
            ]
        installed_issue_priority_ids = BuiltInIssuePriority.objects.all().values_list('id', flat=True)
        self.assertEqual(BuiltInIssuePriority.active_objects.count(), 4)
        for id, type, description in built_in_priorities:
            self.assertIn(uuid.UUID(id), installed_issue_priority_ids)

        # Rerun initializer
        BuiltInIssuePriority.objects.initialize_built_in_issue_priorities()

        # Make sure BuiltInIssuePriority is not duplicated
        installed_issue_priority_ids = BuiltInIssuePriority.objects.all().values_list('id', flat=True)
        self.assertEqual(BuiltInIssuePriority.active_objects.count(), 4)
        for id, type, description in built_in_priorities:
            self.assertIn(uuid.UUID(id), installed_issue_priority_ids)
