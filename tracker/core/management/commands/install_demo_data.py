import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models.organization import Organization, OrganizationData
from core.models.user import CoreUser
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.project import Project, ProjectData, ProjectLabelData, ProjectLabel


def create_core_user(num, users):
    first_names = ["Ada", "Bela", "Cade", "Dax", "Eva", "Fynn", "Gia", "Hugo", "Ivy", "Jax", "John", "Frank", "Zoe", "Liam", "Mia", "Noah", "Olivia", "Emma", "Ava", "Sophia", "Isabella"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark"]
    test_user = {
        'first_name': random.choice(first_names),
        'middle_name': '',
        'last_name': random.choice(last_names),
        'email': f'test_user_{str(num).zfill(2)}@project-tracker.dev',
        'secondary_email': '',
        'home_phone': f'123-456-78{str(num).zfill(2)}',
        'mobile_phone': f'123-456-78{str(num).zfill(2)}',
        'work_phone': f'123-456-78{str(num).zfill(2)}',
        'address_line_1': f'123{str(num).zfill(2)} Main St',
        'address_line_2': '',
        'city': 'Anytown',
        'state': 'NY',
        'postal_code': '12345',
        'country': 'United States',
        'timezone': 'America/Chicago',
        'password': 'password123'
        }
    user = CoreUser.objects.create_core_user_from_web(test_user)

    users.append(user.id)


def create_organization(num, organizations):
    user = CoreUser.objects.get(current__email=f"test_user_{str(num).zfill(2)}@project-tracker.dev")
    organization_random_suffixes = ["Ltd", "Co", "LLC", "Inc", "Group", "Partners", "Associates", "Enterprises", "Industries", "Corporation", "Company", "Ventures", "Holdings", "International", "Global", "Worldwide", "United", "Federation", "Union"]
    organization_random_names = ["Jacob", "Littel-Bayer", "Walter", "Auer and Sons", "Krajcik", "Kirlin", "Wolff-Goodwin", "Williamson-Stark", "Glover Group", "Metz", "Conroy-Lowe", "Ward and Sons", "Schiller", "Toy-Kub", "Moore", "Grant", "Kozey", "Langworth", "Hickle", "Beatty", "Jacobs"]
    organization_name = random.choice(organization_random_names) + " " + random.choice(organization_random_suffixes)
    organization_names = [org.current.name for org in Organization.objects.all()]

    while organization_name in organization_names:
        print("Duplicate organization name found. Trying again...")
        organization_name = random.choice(organization_random_names)

    with transaction.atomic():
        organization_data = OrganizationData.objects.create(
            created_by_id=user.id,
            name=organization_name,
            description=f'This is a test organization number {str(num).zfill(2)}.',
            responsible_party_email=user.current.email,
            responsible_party_phone=user.current.work_phone,
            address_line_1=user.current.address_line_1,
            address_line_2=user.current.address_line_2,
            city=user.current.city,
            state=user.current.state,
            postal_code=user.current.postal_code,
            country=user.current.country,
            timezone=user.current.timezone,
            is_paid=True,
            )
        organization = Organization.objects.create(
            created_by_id=user.id,
            current=organization_data,
            )
        organization.members.add(user)

        organizations.append(organization.id)


def create_project(num, organization_id, user_id, projects):
    user = None
    organization = None
    if organization_id:
        organization = Organization.objects.get(id=organization_id)
        user = organization.members.first()

    if user_id and not user:
        user = CoreUser.objects.get(id=user_id)

    with transaction.atomic():
        project_data = ProjectData.objects.create(
            created_by_id=user.id,
            name=f'Test Project {str(num).zfill(2)}',
            description=f'This is a test project, number {str(num).zfill(2)}.',
            is_active=True,
            )
        project_data.save()
        project = Project.objects.create(
            created_by_id=user.id,
            current=project_data,
            )
        project_label_data = ProjectLabelData.objects.create(
            created_by_id=user.id,
            label=project.generate_label(),
            )
        project_label = ProjectLabel.objects.create(
            created_by_id=user.id,
            current=project_label_data,
            )
        project.users.add(user)
        project.label = project_label
        project.save()

        if organization:
            organization.projects.add(project)

        projects.append(project.id)


def create_git_repository(project_id, repository_name=None, git_repositories=[]):
    project = Project.objects.get(id=project_id)
    if not repository_name:
        repository_name = f'Git Repository for {project.current.name}'
    else:
        repository_name = f'{repository_name} for {project.current.name}'

    with transaction.atomic():
        git_repository_data = GitRepositoryData.objects.create(
            created_by_id=project.created_by_id,
            name=repository_name,
            description=f'This is a git repository for the project {project.current.name}.',
            url='https://github.com/nickrnet/project-tracker',
            )
        git_repository = GitRepository.objects.create(
            created_by_id=project.created_by_id,
            current=git_repository_data,
            )

        project.git_repositories.add(git_repository)
        project.save()

        if project.organizationprojects_set.exists():
            # Typically, a project would only belong to one organization
            organization = project.organizationprojects_set.first()
            organization.git_repositories.add(git_repository)
            organization.save()

        git_repositories.append(git_repository.id)


class Command(BaseCommand):
    # TODO: Refactor this to make is simpler, ditch the noqa bit
    def handle(self, *args, **options):  # noqa
        total_users = 50
        total_organizations = 30
        user_id = None
        users = []
        organizations = []
        projects = []
        git_repositories = []

        self.stdout.write("Flushing database...")
        call_command('flush', '--noinput')
        call_command('setup')

        self.stdout.write("Creating users...")
        for x in range(1, total_users + 1):
            create_core_user(x, users)

        self.stdout.write("Creating organizations...")
        for x in range(1, total_organizations + 1):
            create_organization(x, organizations)

        organization = Organization.objects.get(id=organizations[0])
        self.stdout.write(f"Adding all users to the first organization {organization.id} - {organization.current.name}...")
        for user_id in users:
            user = CoreUser.objects.get(id=user_id)
            organization.members.add(user)
        organization.save()

        self.stdout.write("Creating a personal project per user...")
        for index, user_id in enumerate(users):
            create_project(index + 10000, None, user_id, projects)

        user_id = users[0]
        self.stdout.write(f"Creating 100 personal projects for the first user {user_id}...")
        for y in range(1, 101):
            create_project(y + 20000, None, user_id, projects)

        user_id = users[random.randint(0, total_users - 1)]
        while user_id == users[0]:
            users[random.randint(0, total_users - 1)]

        self.stdout.write(f"Creating 100 personal projects for a randomly selected user {user_id}...")
        for y in range(1, 101):
            create_project(y + 30000, None, user_id, projects)

        self.stdout.write("Creating a project in every organization...")
        for x in range(1, total_organizations + 1):
            organization = Organization.objects.get(id=organizations[x - 1])
            create_project(x + 40000, organization.id, users[0], projects)

        self.stdout.write("Creating projects randomly assigned to organizations...")
        for x in range(1, total_organizations + 1):
            organization = Organization.objects.get(id=organizations[random.randint(0, total_organizations - 1)])
            create_project(x + 50000, organization.id, organization.members.first(), projects)

        self.stdout.write("Adding one git repository to each project...")
        for project in projects:
            create_git_repository(project, None, git_repositories)

        self.stdout.write("Adding 100 git repositories to the first project owned by the first user...")
        for y in range(1, 101):
            create_git_repository(projects[0], f"Git Repository {y + 1000}", git_repositories)

        self.stdout.write("Users with projects:")
        for user_id in users:
            user = CoreUser.objects.get(id=user_id)
            self.stdout.write(f"- {user.current.email} has {user.list_projects().count()} projects.")
