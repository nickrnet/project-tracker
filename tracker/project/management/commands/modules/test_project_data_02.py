from core.management.commands.modules.test_user_data_02 import test_user_02
from core.models import organization as core_organization_models
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models
from project.models import project as project_models


project_data_02 = {
    'name': 'Test Project 02',
    'description': 'This is a test project.',
    'git_repository': None,
    'project_type': None
}


def initialize_test_project_02():
    test_user_02_instance = core_user_models.CoreUser.objects.get(user__email=test_user_02.get('email'))
    test_organization_02_instance = core_organization_models.Organization.objects.get(current__name='Test Organization 02')
    test_git_repository_02_instance = git_repository_models.GitRepository.objects.get(current__name='Test Git Repository 02')

    project_data_02_instance = project_models.ProjectData(
        created_by_id=test_user_02_instance.id,
        name=project_data_02.get('name', ''),
        description=project_data_02.get('description', ''),
    )
    project_data_02_instance.save()
    new_project = project_models.Project(
        created_by_id=test_user_02_instance.id,
        current=project_data_02_instance,
    )
    new_project.save()
    new_project.git_repositories.add(test_git_repository_02_instance)
    new_project.users.add(test_user_02_instance)
    new_project.save()
    test_organization_02_instance.projects.add(new_project)
    test_organization_02_instance.save()
    test_user_02_instance.projects.add(new_project)
    test_user_02_instance.save()
