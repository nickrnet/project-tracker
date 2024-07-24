from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.forms.git_repository import new_git_repository_form as new_git_repository_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


@login_required
def new_git_repository(request):
    if request.method == "POST":
        received_new_git_repository_form = new_git_repository_form.NewGitRepositoryForm(request.POST, request.FILES)
        if received_new_git_repository_form.is_valid():
            received_new_git_repository_form.save(request=request)
            messages.success(request, ('Your git repository was successfully added!'))
        else:
            messages.error(request, 'Error saving git repository.')

        return redirect(reverse("new_git_repository"))

    git_repository_form = new_git_repository_form.NewGitRepositoryForm()
    repositories = git_repository_models.GitRepository.active_objects.all()
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        logged_in_user = None

    return render(request=request, template_name="git_repository/new_git_repository_template.html", context={'logged_in_user': logged_in_user, 'new_git_repository_form': git_repository_form, 'repositories': repositories})
