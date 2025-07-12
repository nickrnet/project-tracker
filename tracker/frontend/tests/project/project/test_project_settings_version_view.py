import uuid

from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from frontend.forms.project.version.version_form import VersionDataForm
from core.models.user import CoreUser
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData
from project.models.version import Version, VersionData


class TestProjectSettingsVersionView(TestCase):
    def setUp(self):
        """
        Creates 2 user, 1 project, with 1 version.
        """
        # Create Users
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})
        self.user2 = CoreUser.objects.create_core_user_from_web({'email': 'testuser2@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

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
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label=self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.version_data1 = VersionData.objects.create(
            created_by=self.user1,
            name="Version 1.0",
            description="Initial Version 1.0 Description",
            label="1.0",
            release_date=timezone.now(),
            is_active=True
            )
        self.version1 = Version.objects.create(
            created_by=self.user1,
            current=self.version_data1,
            project=self.project1
            )

        self.http_client = Client()

    def test_project_settings_version_redirects_if_not_logged_in(self):
        response = self.http_client.get(reverse('project_settings_version', kwargs={'version_id': str(self.version1.id)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project-settings/version/' + str(self.version1.id) + '/')

    def test_project_settings_version_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_version', kwargs={'version_id': str(self.version1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_version_modal.html')

    def test_project_settings_version_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        version_form_data = {
            'name': 'Version 1.0 Modified',
            'description': 'Initial Version 1.0 Description Modified',
            'label': '1.0.0',
            'is_active': False
            }
        version_data = VersionDataForm(version_form_data)
        assert version_data.is_valid() is True, f"Form is not valid: {version_data.errors}"
        form_data = urlencode(version_data.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_version', kwargs={'version_id': str(self.version1.id)}), form_data, url_encoding)
        self.version1.refresh_from_db()
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.assertEqual(self.version1.current.name, 'Version 1.0 Modified')
        self.assertEqual(self.version1.current.description, 'Initial Version 1.0 Description Modified')
        self.assertEqual(self.version1.current.label, '1.0.0')
        self.assertFalse(self.version1.current.is_active)
        self.assertIn('Your version was successfully updated!', str(messages))

    def test_project_settings_version_view_post_to_project_without_label(self):
        self.project1.label = None
        self.project1.save()
        url_encoding = 'application/x-www-form-urlencoded'
        version_form_data = {
            'name': 'Version 1.0 Modified',
            'description': 'Initial Version 1.0 Description Modified',
            'label': '1.0.0',
            'is_active': False
            }
        version_data = VersionDataForm(version_form_data)
        assert version_data.is_valid() is True, f"Form is not valid: {version_data.errors}"
        form_data = urlencode(version_data.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_version', kwargs={'version_id': str(self.version1.id)}), form_data, url_encoding)
        self.version1.refresh_from_db()
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.assertEqual(self.version1.current.name, 'Version 1.0 Modified')
        self.assertEqual(self.version1.current.description, 'Initial Version 1.0 Description Modified')
        self.assertEqual(self.version1.current.label, '1.0.0')
        self.assertFalse(self.version1.current.is_active)
        self.assertIn('Your version was successfully updated!', str(messages))

    def test_project_settings_version_view_post_with_invalid_version_id(self):
        url_encoding = 'application/x-www-form-urlencoded'
        version_form_data = {
            'name': 'Version 1.0 Modified',
            'description': 'Initial Version 1.0 Description Modified',
            'label': '1.0.0',
            'is_active': False
            }
        version_form = VersionDataForm(version_form_data)
        version_form.is_valid()
        form_data = urlencode(version_form.data)
        self.http_client.force_login(user=self.user1.user)
        # Version ID is invalid
        response = self.http_client.post(reverse('project_settings_version', kwargs={'version_id': uuid.UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.version1.refresh_from_db()
        self.assertEqual(self.version1.current.name, 'Version 1.0')
        self.assertEqual(self.version1.current.description, 'Initial Version 1.0 Description')
        self.assertEqual(self.version1.current.label, '1.0')
        self.assertTrue(self.version1.current.is_active)
        self.assertIn('The specified Version does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.', str(messages))

    def test_project_settings_version_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_version', kwargs={'version_id': self.version1.id}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/project/project_settings_modal.html")
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.version1.refresh_from_db()
        self.assertEqual(self.version1.current.name, 'Version 1.0')
        self.assertEqual(self.version1.current.description, 'Initial Version 1.0 Description')
        self.assertEqual(self.version1.current.label, '1.0')
        self.assertTrue(self.version1.current.is_active)
        self.assertIn('Invalid data received. Please try again.', str(messages))

    def test_project_settings_version_view_post_user_no_permission(self):
        url_encoding = 'application/x-www-form-urlencoded'
        version_form_data = {
            'name': 'Version 1.0 Modified',
            'description': 'Initial Version 1.0 Description Modified',
            'label': '1.0.0',
            'is_active': False
            }
        version_form = VersionDataForm(version_form_data)
        version_form.is_valid()
        form_data = urlencode(version_form.data)
        self.http_client.force_login(user=self.user2.user)
        response = self.http_client.post(reverse('project_settings_version', kwargs={'version_id': self.version1.id}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, '/projects')
        # Make sure the form did not update the database
        self.version1.refresh_from_db()
        self.assertEqual(self.version1.current.name, 'Version 1.0')
        self.assertEqual(self.version1.current.description, 'Initial Version 1.0 Description')
        self.assertEqual(self.version1.current.label, '1.0')
        self.assertTrue(self.version1.current.is_active)
        self.assertIn('The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.', str(messages))
