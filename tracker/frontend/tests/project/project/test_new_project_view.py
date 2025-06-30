from datetime import datetime

from django.contrib.messages import get_messages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.project import Project

from frontend.forms.project.project.new_project_form import NewProjectForm


class TestNewProjectView(TestCase):
    def setUp(self):
        """
        Creates 1 user, 1 organization, 1 git repository.
        """

        self.system_user = CoreUser.objects.get_or_create_system_user()
        self.user1 = CoreUser.objects.create_core_user_from_web({'email': 'testuser1@project-tracker.dev', 'password': 'password', 'timezone': 'EST'})

        self.organization1_data = OrganizationData.objects.create(
            created_by_id=self.user1.id,
            name='Test Organization 1',
            address_line_1='123 Main St',
            address_line_2='',
            city='Anytown',
            state='NY',
            postal_code='12345',
            country='USA',
            timezone='America/Chicago',
            responsible_party_email=self.user1.current.email,
            responsible_party_phone=self.user1.current.work_phone,
            )
        self.organization1 = Organization.objects.create(
            created_by_id=self.user1.id,
            current=self.organization1_data,
            )
        self.organization1.members.add(self.user1)
        self.organization1.save()

        self.git_repository1_data = GitRepositoryData.objects.create(
            created_by=self.user1,
            name="Initial Repo 1",
            description="Initial Repo 1 Description",
            url="https://github.com/example/repo1"
            )
        self.git_repository1_data.save()
        self.git_repository1 = GitRepository.objects.create(created_by=self.user1, current=self.git_repository1_data)

        self.http_client = Client()

    def test_new_project_view_redirects_when_not_logged_in(self):
        response = self.http_client.get(reverse('new_project'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/new_project')

    def test_new_project_view_get(self):
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.get(reverse('new_project'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/new_project_modal.html')

    def test_new_project_post(self):
        url_encoding = 'application/x-www-form-urlencoded'
        start_date = timezone.now().strftime("%m/%d/%Y")
        end_date = timezone.now().strftime("%m/%d/%Y")
        new_project_form_data = {
            'name': 'Test Project 1',
            'description': 'Test Project Description 1',
            'label': 'test-project-1',
            'is_active': True,
            'is_private': False,
            'start_date': start_date,
            'end_date': end_date,
            'git_repository': str(self.git_repository1.id),
            # 'organization': str(self.organization1.id),  # TODO: BUG: This is not handled in the view
            }
        new_project_form = NewProjectForm(new_project_form_data)
        new_project_form.is_valid()
        form_data = urlencode(new_project_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_project'), form_data, url_encoding)
        project = Project.objects.first()
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/projects_table.html')
        # Make sure the whole form came through to the database
        self.assertEqual(project.current.name, 'Test Project 1')
        self.assertEqual(project.current.description, 'Test Project Description 1')
        self.assertEqual(project.current.is_active, True)
        self.assertEqual(project.current.is_private, False)
        self.assertEqual(project.current.start_date, datetime.strptime(start_date, '%m/%d/%Y').date())
        self.assertEqual(project.current.end_date, datetime.strptime(end_date, '%m/%d/%Y').date())
        self.assertEqual(project.label.current.label, 'test-project-1')
        self.assertIn(self.git_repository1, project.git_repositories.all())
        self.assertIn(self.user1, project.users.all())
        self.assertIn('Your project was successfully added!', str(messages))

    def test_new_project_post_without_git_repository(self):
        url_encoding = 'application/x-www-form-urlencoded'
        start_date = timezone.now()  # TODO: Need to format these to MM/DD/YY
        end_date = timezone.now()
        new_project_form_data = {
            'name': 'Test Project 1',
            'description': 'Test Project Description 1',
            'label': 'test-project-1',
            'is_active': True,
            'is_private': False,
            # 'start_date': start_date,
            # 'end_date': end_date,
            # 'organization': str(self.organization1.id),  # TODO: BUG: This is not handled in the view
            }
        new_project_form = NewProjectForm(new_project_form_data)
        new_project_form.is_valid()
        form_data = urlencode(new_project_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_project'), form_data, url_encoding)
        project = Project.objects.first()
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/projects_table.html')
        # Make sure the whole form came through to the database
        self.assertEqual(project.current.name, 'Test Project 1')
        self.assertEqual(project.current.description, 'Test Project Description 1')
        self.assertEqual(project.current.is_active, True)
        self.assertEqual(project.current.is_private, False)
        self.assertEqual(project.current.start_date, datetime.strptime(start_date, '%m/%d/%Y').date())
        self.assertEqual(project.current.end_date, datetime.strptime(end_date, '%m/%d/%Y').date())
        self.assertEqual(project.label.current.label, 'test-project-1')
        self.assertNotIn(self.git_repository1, project.git_repositories.all())
        self.assertIn(self.user1, project.users.all())
        self.assertIn('Your project was successfully added!', str(messages))

    def test_new_project_post_without_project_label(self):
        url_encoding = 'application/x-www-form-urlencoded'
        start_date = timezone.now()  # TODO: Need to format these to MM/DD/YYYY
        end_date = timezone.now()
        new_project_form_data = {
            'name': 'Test Project 1',
            'description': 'Test Project Description 1',
            'is_active': True,
            'is_private': False,
            # 'start_date': start_date,
            # 'end_date': end_date,
            # 'organization': str(self.organization1.id),  # TODO: BUG: This is not handled in the view
            }
        new_project_form = NewProjectForm(new_project_form_data)
        new_project_form.is_valid()
        form_data = urlencode(new_project_form.data)
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_project'), form_data, url_encoding)
        project = Project.objects.first()
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/projects_table.html')
        # Make sure the whole form came through to the database
        self.assertEqual(project.current.name, 'Test Project 1')
        self.assertEqual(project.current.description, 'Test Project Description 1')
        self.assertEqual(project.current.is_active, True)
        self.assertEqual(project.current.is_private, False)
        self.assertEqual(project.current.start_date, datetime.strptime(start_date, '%m/%d/%Y').date())
        self.assertEqual(project.current.end_date, datetime.strptime(end_date, '%m/%d/%Y').date())
        self.assertIsNone(project.label)
        self.assertNotIn(self.git_repository1, project.git_repositories.all())
        self.assertIn(self.user1, project.users.all())
        self.assertIn('Your project was successfully added!', str(messages))

    def test_new_project_post_with_bad_form(self):
        url_encoding = 'application/x-www-form-urlencoded'
        form_data = 'a=1'
        self.http_client.force_login(user=self.user1.user)
        response = self.http_client.post(reverse('new_project'), form_data, url_encoding)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project/projects_table.html')
        self.assertIn('Error saving project.', str(messages))
        # Make sure the form did not save to the database
        self.assertEqual(Project.objects.count(), 0)
