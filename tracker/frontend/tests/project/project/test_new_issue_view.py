from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.issue import Issue
from project.models.issue_type import BuiltInIssueType
from project.models.priority import BuiltInIssuePriority
from project.models.status import BuiltInIssueStatus
from project.models.severity import BuiltInIssueSeverity
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData
from project.models.component import Component, ComponentData
from project.models.version import Version, VersionData

from frontend.forms.project.issue.new_issue_form import NewIssueForm


class TestNewIssueView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 project, 1 version, 1 component, and the built-in Issue requirements.
        """

        self.system_user = CoreUser.objects.get_or_create_system_user()
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})
        BuiltInIssueType.objects.initialize_built_in_types()
        BuiltInIssuePriority.objects.initialize_built_in_priorities()
        BuiltInIssueStatus.objects.initialize_built_in_statuses()
        BuiltInIssueSeverity.objects.initialize_built_in_severities()

        self.issue_type_bug = BuiltInIssueType.objects.get(type='BUG')
        self.issue_priority_low = BuiltInIssuePriority.objects.get(name='LOW')
        self.issue_status_triage = BuiltInIssueStatus.objects.get(name='TRIAGE')
        self.issue_severity_minor = BuiltInIssueSeverity.objects.get(name='MINOR')

        self.project1_label_data = ProjectLabelData.objects.create(
            created_by=self.user1,
            label='project01',
            description='Project 01 Label'
        )
        self.project1_label = ProjectLabel.objects.create(created_by=self.user1, current=self.project1_label_data)

        self.project1_data = ProjectData.objects.create(
            created_by=self.user1,
            name='Initial Project 1',
            description='Initial Project 1 Description',
            start_date=timezone.now(),
            is_active=True
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label = self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.version1_data = VersionData.objects.create(
            created_by=self.user1,
            name='1.0.0',
            label='1.0.0',
            release_date=timezone.now(),
            is_active=True
        )
        self.version1 = Version.objects.create(
            created_by=self.user1,
            current=self.version1_data,
            project=self.project1
        )

        self.component1_data = ComponentData.objects.create(
            created_by=self.user1,
            name='Component1',
            is_active=True
        )
        self.component1 = Component.objects.create(
            created_by=self.user1,
            current=self.component1_data,
            project=self.project1
        )

        self.http_client = Client()

    def test_new_issue_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('new_project_issue', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project/new_issue/' + str(self.project1.id) + '/')

    def test_new_issue_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('new_project_issue', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/new_issue_modal.html')

    def test_new_issue_view_get_with_project_label(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('new_project_issue', kwargs={'project_id': self.project1.label.current.label}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/new_issue_modal.html')

    def test_new_issue_view_get_with_project_label_that_does_not_exist(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('new_project_issue', kwargs={'project_id': 'this_project_does_not_exist'}))
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, reverse('projects'))
        self.assertIn('Choose a project.', str(messages))

    def test_new_issue_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        new_issue_form_data = {
            'summary': 'Issue Summary 1',
            'description': 'Issue Description 1',
            'project': str(self.project1.id),
            'reporter': str(self.user1.id),
            'assignee': str(self.user1.id),
            'watchers': '',
            'built_in_type': str(self.issue_type_bug.id),
            'built_in_priority': str(self.issue_priority_low.id),
            'built_in_status': str(self.issue_status_triage.id),
            'built_in_severity': str(self.issue_severity_minor.id),
            'version': str(self.version1.id),
            'component': str(self.component1.id)
        }
        new_issue_form = NewIssueForm(new_issue_form_data)
        new_issue_form.is_valid()
        form_data = urlencode(new_issue_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_project_issue', kwargs={'project_id': self.project1.label.current.label}), form_data, url_encoding)
        issue = Issue.objects.first()
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/issues_table.html')
        # Make sure the whole form came through to the database
        self.assertEqual(issue.current.summary, 'Issue Summary 1')
        self.assertEqual(issue.current.description, 'Issue Description 1')
        self.assertEqual(issue.current.project, self.project1)
        self.assertEqual(issue.current.reporter, self.user1)
        self.assertEqual(issue.current.assignee, self.user1)
        self.assertEqual(issue.current.built_in_type, self.issue_type_bug)
        self.assertEqual(issue.current.built_in_priority, self.issue_priority_low)
        self.assertEqual(issue.current.built_in_status, self.issue_status_triage)
        self.assertEqual(issue.current.built_in_severity, self.issue_severity_minor)
        self.assertEqual(issue.current.version, self.version1)
        self.assertEqual(issue.current.component, self.component1)
        self.assertIn('Your issue was successfully added!', str(messages))

    def test_new_issue_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'a=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_project_issue', kwargs={'project_id': self.project1.label.current.label}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/issues_table.html')
        self.assertIn('Error saving issue.', str(messages))
        # Make sure the form did not save to the database
        self.assertEqual(Issue.objects.count(), 0)
