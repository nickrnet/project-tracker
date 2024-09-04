from core.management.commands.modules.test_user_data_02 import test_user_02
from core.models import organization as core_organization_models
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


test_git_repository_02 = {
    'name': 'Test Git Repository 02',
    'description': 'This is a test git repository.',
    'url': ''
}


def initialize_test_git_repository_02():
    test_user_02_instance = core_user_models.CoreUser.objects.get(user__email=test_user_02.get('email'))
    test_organization_02_instance = core_organization_models.Organization.objects.get(current__name='Test Organization 02')

    git_repository_data = git_repository_models.GitRepositoryData(
        created_by_id=test_user_02_instance.id,
        name=test_git_repository_02.get('name', ''),
        description=test_git_repository_02.get('description', ''),
        url=test_git_repository_02.get('url', ''),
    )
    git_repository_data.save()
    new_git_repository = git_repository_models.GitRepository(
        created_by_id=test_user_02_instance.id,
        current=git_repository_data,
    )
    new_git_repository.save()
    test_organization_02_instance.repositories.add(new_git_repository)
    test_organization_02_instance.save()
    test_user_02_instance.git_repositories.add(new_git_repository)
    test_user_02_instance.save()
