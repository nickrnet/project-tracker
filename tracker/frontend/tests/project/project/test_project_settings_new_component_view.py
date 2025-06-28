from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from frontend.forms.project.component.new_component_form import NewComponentDataForm
from core.models.user import CoreUser
from project.models import component as component_models
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData

class TestProjectSettingsNewGitRepositoryView(TestCase):
    def setUp(self):
        """
        Creates 2 user, 1 project.
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
            is_active=True
            )
        self.project1 = Project.objects.create(created_by=self.user1, current=self.project1_data, label = self.project1_label)
        self.project1.users.add(self.user1)
        self.project1.save()

        self.http_client = Client()

    def test_project_settings_new_component_redirects_if_not_logged_in(self):
        response = self.http_client.get(reverse('project_settings_new_component'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project-settings/new-component/')

    def test_project_settings_new_component_view_get_if_no_project_id(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_new_component'))
        self.assertEqual(response.status_code, 302)
        # Does this redirect somewhere?

    def test_project_settings_new_component_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_new_component', kwargs={'project_id':self.project1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_new_component_modal.html')

    def test_project_settings_new_component_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        component_form_data = {
            'name' : 'Component 1',
            'description' : 'First Component Description',
            'label' : 'Primary',
            'is_active' : True
        }
        component_form = NewComponentDataForm(component_form_data)
        component_form.is_valid()
        form_data = urlencode(component_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_new_component',kwargs={'project_id':self.project1.id}), form_data, url_encoding)
        component = component_models.Component.objects.first()
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.assertEqual(component.current.name, 'Component 1')
        self.assertEqual(component.current.description, 'First Component Description')
        self.assertEqual(component.current.label, 'Primary')
        self.assertEqual(component.current.is_active, True)
        self.assertIn('Your component was successfully added!', str(messages))

    def test_project_settings_new_component_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_new_component',kwargs={'project_id':self.project1.id}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/project/project_settings_modal.html")
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(component_models.Component.objects.count(), 0)
        self.assertIn('Invalid data received. Please try again.', str(messages))

    def test_project_settings_new_component_view_post_user_no_permission(self):
        url_encoding = 'application/x-www-form-urlencoded'
        component_form_data = {
            'name' : 'Component 1',
            'description' : 'First Component Description',
            'label' : 'Primary',
            'is_active' : True
        }
        component_form = NewComponentDataForm(component_form_data)
        component_form.is_valid()
        form_data = urlencode(component_form.data)
        self.http_client.force_login(user=self.user2.user)
        response = self.http_client.post(reverse('project_settings_new_component',kwargs={'project_id':self.project1.id}), form_data, url_encoding)
        component = component_models.Component.objects.first()
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, '/projects')
        # Make sure the form did not update the database
        self.assertEqual(component_models.Component.objects.count(), 0)
        self.assertIn('Permission denied.', str(messages))