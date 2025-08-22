from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.issue import Issue, IssueData
from project.models.issue_type import BuiltInIssueType
from project.models.priority import BuiltInIssuePriority
from project.models.status import BuiltInIssueStatus
from project.models.severity import BuiltInIssueSeverity
from project.models.status import BuiltInIssueStatus
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData

from frontend.forms.project.git_repository.git_repository_form import GitRepositoryDataForm


class TestIssueView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 project, 1 issue, and the built-in Issue requirements.
        """

        self.system_user = CoreUser.objects.get_or_create_system_user()
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})
        BuiltInIssueType.objects.initialize_built_in_types()
        BuiltInIssuePriority.objects.initialize_built_in_priorities()
        BuiltInIssueStatus.objects.initialize_built_in_statuses()
        BuiltInIssueSeverity.objects.initialize_built_in_severities()

        self.issue_type_bug = BuiltInIssueType.objects.get(type='BUG')
        self.issue_type_priority = BuiltInIssuePriority.objects.get(name='LOW')
        self.issue_type_status = BuiltInIssueStatus.objects.get(name='TRIAGE')
        self.issue_type_severity = BuiltInIssueSeverity.objects.get(name='MINOR')

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
            is_active=True
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label = self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()
        self.issue_data1 = IssueData.objects.create(
            created_by=self.user1,
            reporter=self.user1,
            summary="Issue 1",
            description="Description for issue 1",
            project=self.project1,
            built_in_type=self.issue_type_bug,
            built_in_priority=self.issue_type_priority,
            built_in_status=self.issue_type_status,
            built_in_severity=self.issue_type_severity,
            # custom_type='',
            # custom_priority='',
            # custom_severity='',
            # custom_status='',
            # component=UUID,
            # version=UUID,
            )
        self.issue1 = Issue.objects.create(
            created_by=self.user1,
            sequence=1,
            current=self.issue_data1,
            project=self.project1
            )

        self.http_client = Client()

    def test_issue_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('issue', kwargs={'issue_id': str(self.issue1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/issue/' + str(self.issue1.id) + '/')

    def test_issue_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('issue', kwargs={'issue_id': str(self.issue1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/issue/issue_modal.html')
