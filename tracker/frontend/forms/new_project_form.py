from django import forms

from . import new_git_repository_form as new_git_repository_form
from core.models import user as core_user_models
from project.models import project as project_models


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = project_models.Project
        fields = [
            'name', 'description', 'is_active', 'is_private', 'start_date', 'end_date', 'git_repository',
        ]

    git_repository = new_git_repository_form.NewGitRepositoryForm()

    def save(self, request):
        project = super(NewProjectForm, self).save(commit=False)
        try:
            logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
        except core_user_models.CoreUser.DoesNotExist:
            print("User does not exist.")
            return None

        project.created_by = logged_in_user
        project.save()
        return project
