from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.forms import new_git_repository_form as new_git_repository_form
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

    return render(request=request, template_name="new_git_repository_template.html", context={'new_git_repository_form': git_repository_form, 'repositories': repositories})
