from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models.user import CoreUser
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData


class TestProjectSettingsUserSelectView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 project with label.
        """

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
            is_active=True,
            is_private=False
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label=self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.users.add(self.user2)
        self.project1.save()

        self.http_client = Client()

    def test_project_settings_user_select_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('project_settings_user_select', kwargs={'project_id': str(self.project1.label)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/' + str(self.project1.label) + '/project-settings/user-select/')

    def test_project_settings_user_select_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_user_select', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_user_select_modal.html')

    def test_project_settings_user_select_view_get_with_bad_project_id(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_user_select', kwargs={'project_id': '4e6089a5-c16d-4642-8576-62204be7cc13'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/projects')

    def test_project_settings_user_select_view_get_without_project_label(self):
        self.project1.label = None
        self.project1.save()
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_user_select', kwargs={'project_id': str(self.project1.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_user_select_modal.html')

    def test_project_settings_user_select_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'current_users=' + str(self.user1.id)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_user_select', kwargs={'project_id': str(self.project1.label)}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        # Make sure the form came through to the database and only changed the project users
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.current.name, 'Initial Project 1')
        self.assertEqual(self.project1.current.description, 'Initial Project 1 Description')
        self.assertEqual(self.project1.current.is_active, True)
        self.assertEqual(self.project1.current.is_private, False)
        self.assertEqual(self.project1.users.count(), 1)
        self.assertIn(self.user1, self.project1.users.all())
        self.assertNotIn(self.user2, self.project1.users.all())
        self.assertIn('Project users updated successfully!', str(messages))

    def test_project_settings_user_select_view_post_without_label(self):
        url_encoding = 'application/x-www-form-urlencoded'
        self.project1.label = None
        self.project1.save()
        form_data = 'current_users=' + str(self.user1.id)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_user_select', kwargs={'project_id': str(self.project1.id)}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form came through to the database and only changed the project users
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.current.name, 'Initial Project 1')
        self.assertEqual(self.project1.current.description, 'Initial Project 1 Description')
        self.assertEqual(self.project1.current.is_active, True)
        self.assertEqual(self.project1.current.is_private, False)
        self.assertIn('Project users updated successfully!', str(messages))

    def test_project_settings_user_select_view_post_with_bad_project_label(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'current_users=' + str(self.user1.id)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_user_select', kwargs={'project_id': 'awesome-project'}), form_data, url_encoding)
        self.assertRedirects(response, reverse('projects'))
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.users.count(), 2)  # Users were not added/removed
        self.assertIn(self.user1, self.project1.users.all())
        self.assertIn(self.user2, self.project1.users.all())
        self.assertIn('The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.', str(messages))

    def test_project_settings_user_select_view_post_with_invalid_users(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'current_users=b5de211e-97f1-4119-98df-5827d56ca12f&current_users=39f44dc9-5d81-4e57-a4f7-559d0f89a245'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_user_select', kwargs={'project_id': self.project1.id}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.users.count(), 2)  # Users were not added/removed
        self.assertIn(self.user1, self.project1.users.all())
        self.assertIn(self.user2, self.project1.users.all())
        self.assertIn('Error updating project users.', str(messages))

    def test_project_settings_user_select_view_post_empty_list(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_user_select', kwargs={'project_id': str(self.project1.label)}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_modal.html')
        # Make sure the form came through to the database and only changed the project users
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.current.name, 'Initial Project 1')
        self.assertEqual(self.project1.current.description, 'Initial Project 1 Description')
        self.assertEqual(self.project1.current.is_active, True)
        self.assertEqual(self.project1.current.is_private, False)
        self.assertEqual(self.project1.users.count(), 0)
        self.assertNotIn(self.user1, self.project1.users.all())
        self.assertNotIn(self.user2, self.project1.users.all())
        self.assertIn('Project users updated successfully!', str(messages))
