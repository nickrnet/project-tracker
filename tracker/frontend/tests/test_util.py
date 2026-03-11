from django.test import TestCase
from django.utils import timezone

from frontend.util.project import get_project_by_uuid_or_label

from core.models import user as core_user_models
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData


class FrontendUtilProjectTestCase(TestCase):
    def setUp(self):
        self.user1 = core_user_models.CoreUser.objects.create_core_user_from_web({'email': 'test_user1@project-tracker.dev', 'password': 'password'})
        self.user2 = core_user_models.CoreUser.objects.create_core_user_from_web({'email': 'test_user2@project-tracker.dev', 'password': 'password'})

        self.project1_label_data = ProjectLabelData.objects.create(
            created_by=self.user1,
            label='project01',
            description='Project 01 Label'
            )
        self.project1_label = ProjectLabel.objects.create(created_by=self.user1, current=self.project1_label_data)

        self.project1_data = ProjectData.objects.create(
            created_by=self.user1,
            name="Initial Project 1",
            description="Initial Project 1 Description",
            start_date=timezone.now(),
            is_active=True,
            is_private=False
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label=self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()

    def test_get_project_by_uuid_or_label_by_label(self):
        project = get_project_by_uuid_or_label(self.user1, self.project1_label_data.label)
        self.assertEqual(project, self.project1)

    def test_get_project_by_uuid_or_label_by_uuid(self):
        project = get_project_by_uuid_or_label(self.user1, str(self.project1.id))
        self.assertEqual(project, self.project1)

    def test_get_project_by_uuid_or_label_empty(self):
        project = get_project_by_uuid_or_label(self.user1, '')
        self.assertIsNone(project)

    def test_get_project_by_uuid_or_label_uuid_does_not_exist(self):
        project = get_project_by_uuid_or_label(self.user1, 'b273b20a-3e15-4ad0-b7e1-4ab90a7a76ba')
        self.assertIsNone(project)

    def test_get_project_by_uuid_or_label_user_cannot_access(self):
        project = get_project_by_uuid_or_label(self.user2, self.project1_label_data.label)
        self.assertIsNone(project)
