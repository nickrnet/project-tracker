from django import forms

from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


class NewGitRepositoryForm(forms.ModelForm):
    class Meta:
        model = git_repository_models.GitRepository
        fields = [
            'name', 'description', 'url',
        ]

    def save(self, request):
        git_repository = super(NewGitRepositoryForm, self).save(commit=False)
        try:
            logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
        except core_user_models.CoreUser.DoesNotExist:
            print("User does not exist.")
            return None

        git_repository.created_by = logged_in_user
        git_repository.save()
        return git_repository
