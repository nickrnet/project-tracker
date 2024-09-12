from core.management.commands.modules.test_user_data_01 import test_user_01
from core.models import organization as core_organization_models
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


test_git_repository_01 = {
    'name': 'Test Git Repository 01',
    'description': 'This is a test git repository.',
    'url': 'https://github.com/nickrnet/project-tracker'
}


def initialize_test_git_repository_01():
    test_user_01_instance = core_user_models.CoreUser.objects.get(user__email=test_user_01.get('email'))
    test_organization_01_instance = core_organization_models.Organization.objects.get(current__name='Test Organization 01')

    git_repository_data = git_repository_models.GitRepositoryData(
        created_by_id=test_user_01_instance.id,
        name=test_git_repository_01.get('name', ''),
        description=test_git_repository_01.get('description', ''),
        url=test_git_repository_01.get('url', ''),
    )
    git_repository_data.save()
    new_git_repository = git_repository_models.GitRepository(
        created_by_id=test_user_01_instance.id,
        current=git_repository_data,
    )
    new_git_repository.save()
    test_organization_01_instance.git_repositories.add(new_git_repository)
    test_organization_01_instance.save()
