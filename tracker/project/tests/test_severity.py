import uuid

from django.test import TestCase

from project.models.severity import BuiltInIssueSeverity


class TestBuiltInIssueSeverityActiveManager(TestCase):
    def setUp(self):
        BuiltInIssueSeverity.objects.initialize_built_in_issue_severities()

    def test_built_in_issue_priority_initializer(self):
        built_in_issue_severities = [
            ('8e0432d7-81c6-4a3d-a5c8-a2dfbba1b330', 'CRITICAL', 'Critical'),
            ('9aaa5bfe-3150-4db1-ad02-ee47694f569b', 'MAJOR', 'Major'),
            ('e82b1549-0beb-44ee-926b-d03b5dd95aa7', 'MINOR', 'Minor'),
            ]
        installed_issue_severity_ids = BuiltInIssueSeverity.objects.all().values_list('id', flat=True)
        self.assertEqual(BuiltInIssueSeverity.active_objects.count(), 3)
        for id, type, description in built_in_issue_severities:
            self.assertIn(uuid.UUID(id), installed_issue_severity_ids)

        # Rerun initializer
        BuiltInIssueSeverity.objects.initialize_built_in_issue_severities()

        # Make sure BuiltInIssueSeverity is not duplicated
        installed_issue_severity_ids = BuiltInIssueSeverity.objects.all().values_list('id', flat=True)
        self.assertEqual(BuiltInIssueSeverity.active_objects.count(), 3)
        for id, type, description in built_in_issue_severities:
            self.assertIn(uuid.UUID(id), installed_issue_severity_ids)
