from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from core.models.user import CoreUser
from project.models.project import Project, ProjectData, ProjectLabel, ProjectLabelData
from project.models import component as component_models
from project.models.component import Component, ComponentData

from frontend.forms.project.component.component_form import ComponentDataForm

class TestProjectSettingsComponentView(TestCase):
    def setUp(self):
        """
        Creates 2 user, 2 project with 1 component
        """
        # Create Users
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})
        self.user2 = CoreUser.objects.create_core_user_from_web({'email': 'testuser2@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

        # Create Project 1
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

        # Create Components for Project 1
        self.component1_data = ComponentData.objects.create(
            created_by=self.user1,
            name="Component 1",
            description="Description of Component 1",
            label="Component 1 Label",
            is_active=True
        )
        self.component1 = Component.objects.create(
            created_by=self.user1,
            current=self.component1_data, 
            project=self.project1
        )

        # TODO - Delete project2 if reworking get_project() method, this is only used in test_project_settings_component_view_post_project_id_is_label()
        # Also if deleted, adjust assertions to 1 component in component_models.Component.objects

        # Create Project 2
        self.project2_label_data = ProjectLabelData.objects.create(
            created_by=self.user2,
            label='project02',
            description='Project 02 Label'
        )
        self.project2_label = ProjectLabel.objects.create(created_by=self.user2, current=self.project2_label_data)

        self.project2_data = ProjectData.objects.create(
            created_by=self.user2,
            name="Initial Project 2",
            description="Initial Project 2 Description",
            start_date=timezone.now(),
            is_active=True
            )
        self.project2 = Project.objects.create(created_by=self.user2, current=self.project2_data, label = self.project2_label)
        self.project2.users.add(self.user2)
        self.project2.save()

        # Create Component for Project 2
        self.component2_data = ComponentData.objects.create(
            created_by=self.user2,
            name="Component 2",
            description="Description of Component 2",
            label="Component 2 Label",
            is_active=True
        )
        self.component2 = Component.objects.create(
            created_by=self.user2,
            current=self.component2_data, 
            project=self.project2
        )

        # Create Client
        self.http_client = Client()

    def test_project_settings_component_redirects_if_not_logged_in(self):
        response = self.http_client.get(reverse('project_settings_component'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/project-settings/component/')

    def test_project_settings_component_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('project_settings_component', kwargs={'component_id':self.component1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/project_settings_component_modal.html')
    
    # TODO - This test doesn't dive into lines 20-23 of the view as intended... look into UUID corruption or rework get_project() method
    def test_project_settings_component_view_post_project_id_is_label(self):
        # Make Project with improper UUID
        self.project2.id = "1234-asdf"
        url_encoding = 'application/x-www-form-urlencoded'
        component_form_data = {
            'name' : 'Component 2',
            'description' : 'Description of Component 2',
            'label' : 'Component 2 Label',
            'is_active' : True
        }
        component_form = ComponentDataForm(component_form_data)
        component_form.is_valid()
        form_data = urlencode(component_form.data)
        self.http_client.force_login(user=self.user2.user)
        response = self.http_client.post(reverse('project_settings_component', kwargs={'component_id':self.component2.id}), form_data, url_encoding)
        component = component_models.Component.objects.last()
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.assertEqual(component.current.name, 'Component 2')
        self.assertEqual(component.current.description, 'Description of Component 2')
        self.assertEqual(component.current.label, 'Component 2 Label')
        self.assertEqual(component.current.is_active, True)
        self.assertIn('Your component was successfully updated!', str(messages))

    def test_project_settings_component_view_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        component_form_data = {
            'name' : 'Component 1',
            'description' : 'Description of Component 1',
            'label' : 'Component 1 Label',
            'is_active' : True
        }
        component_form = ComponentDataForm(component_form_data)
        component_form.is_valid()
        form_data = urlencode(component_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_component', kwargs={'component_id':self.component1.id}), form_data, url_encoding)
        component = component_models.Component.objects.first()
        messages = list(get_messages(response.wsgi_request))
        # Make sure the whole form came through to the database
        self.assertEqual(component.current.name, 'Component 1')
        self.assertEqual(component.current.description, 'Description of Component 1')
        self.assertEqual(component.current.label, 'Component 1 Label')
        self.assertEqual(component.current.is_active, True)
        self.assertIn('Your component was successfully updated!', str(messages))

    def test_project_settings_component_view_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'foo=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('project_settings_component', kwargs={'component_id':self.component1.id}), form_data, url_encoding)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/project/project_settings_modal.html")
        messages = list(get_messages(response.wsgi_request))
        # Make sure the form did not update the database
        self.assertEqual(component_models.Component.objects.count(), 2)
        self.assertIn('Invalid data received. Please try again.', str(messages))

    def test_project_settings_component_view_post_user_no_permission(self):
        url_encoding = 'application/x-www-form-urlencoded'
        component_form_data = {
            'name' : 'Component 1',
            'description' : 'Description of Component 1',
            'label' : 'Component 1 Label',
            'is_active' : True
        }
        component_form = ComponentDataForm(component_form_data)
        component_form.is_valid()
        form_data = urlencode(component_form.data)
        self.http_client.force_login(user=self.user2.user)
        response = self.http_client.post(reverse('project_settings_component', kwargs={'component_id':self.component1.id}), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, '/projects')
        # Make sure the form did not update the database
        self.assertEqual(component_models.Component.objects.count(), 2)
        self.assertIn('Permission denied.', str(messages))