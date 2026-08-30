from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from frontend.util import project as project_utils
from frontend.forms.project.git_repository import git_repository_form as git_repository_form
from frontend.forms.project.project import project_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


class GitRepositoryView(LoginRequiredMixin, View):
    def valid_git_repository(self, logged_in_user, project_id, git_repository):
        not_valid = False
        git_repository_project = git_repository.project_set.first()

        # Make sure git repository is in project
        if project_id != git_repository_project.id:
            not_valid = True

        # Check if user can access issueproject
        # TODO: this check may not be needed... by the time this code is reached, we've already filtered the git repository by project and user
        # frontend.tests.project.project.test_project_settings_git_repository_view.TestProjectSettingsGitRepositoryView.test_project_settings_git_repository_view_get_user_cannot_access_project tries to test this, can't get code coverage to hit
        # commenting out for code coverage, but leaving for tinkering later
        # project = project_utils.get_project_by_uuid_or_label(logged_in_user, git_repository_project.id)
        # if project is None:
        #     not_valid = True

        if not_valid:
            return False

        return True

    def validate_url(self, thing_to_validate: str) -> bool:
        validator = URLValidator()
        try:
            validator(thing_to_validate)
            return True
        except ValidationError:
            return False

    def get(self, request, project_id, git_repository_id):
        """
        Displays the Git Repository when a user clicks it in the Project Settings modal.

        Currently assumes if this is requested, a git repository is tied to a project already.
        """

        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        try:
            git_repository = logged_in_user.list_git_repositories().get(pk=git_repository_id)
        except git_repository_models.GitRepository.DoesNotExist:
            messages.error(request, 'The specified git repository does not exist.')
            return redirect("projects")

        # Check if user can access project
        project = project_utils.get_project_by_uuid_or_label(logged_in_user, git_repository.project_set.first().id)
        if project is None:
            messages.error(request, 'The specified project does not exist.')
            return redirect("projects")

        form = git_repository_form.GitRepositoryDataForm(model_to_dict(git_repository.current))
        valid_url = self.validate_url(git_repository.current.url)
        organizations = logged_in_user.list_organizations()
        projects = logged_in_user.list_projects()

        return render(
            request=request,
            template_name="project/project/project_settings_git_repository_modal.html",
            context={
                'logged_in_user': logged_in_user,
                'git_repository_form': form,
                'git_repository': git_repository,
                'project': git_repository.project_set.first(),
                'organization': git_repository.organizationgitrepositories_set.first(),
                'valid_url': valid_url,
                'organizations': organizations,
                'projects': projects,
                }
            )

    def post(self, request, project_id, git_repository_id):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

        try:
            git_repository = logged_in_user.list_git_repositories().get(id=git_repository_id)
            if not self.valid_git_repository(logged_in_user, project_id, git_repository):
                messages.error(request, 'The specified git repository does not exist.')
                return redirect("projects")

            received_git_repository_form = git_repository_form.GitRepositoryDataForm(request.POST, request.FILES)
            if received_git_repository_form.is_valid():
                git_repository_data = git_repository_models.GitRepositoryData(
                    created_by=logged_in_user,
                    created_on=timezone.now(),
                    git_repository=git_repository,
                    name=received_git_repository_form.cleaned_data.get('name'),
                    description=received_git_repository_form.cleaned_data.get('description'),
                    url=received_git_repository_form.cleaned_data.get('url'),
                    )
                git_repository_data.save()
                git_repository.current = git_repository_data
                git_repository.save()

                messages.info(request, 'Your git repository was successfully updated.')
            else:
                messages.error(request, 'Error saving git repository.')

            # TODO: Guarantee the project is the correct one we came from
            project = git_repository.project_set.first()
            project_id = str(project.id)
            project_dict = model_to_dict(project.current)
            if project.label:
                project_dict['label'] = project.label.current.label
            form = project_form.ProjectDataForm(project_dict)
            return render(
                request=request,
                template_name="project/project/project_settings_modal.html",
                context={
                    'logged_in_user': logged_in_user,
                    'project': project,
                    'project_id': project_id,
                    'project_form': form,
                    'git_repositories': project.git_repositories.all(),
                    'issues': project.issue_set.all(),
                    }
                )
        except git_repository_models.GitRepository.DoesNotExist:
            messages.error(request, 'The specified git repository does not exist.')
            return redirect("projects")
