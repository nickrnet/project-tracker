from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from frontend.forms.project.git_repository import new_git_repository_form as new_git_repository_form
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models


@login_required
def new_git_repository(request):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        received_new_git_repository_data_form = new_git_repository_form.NewGitRepositoryDataForm(request.POST, request.FILES)
        if received_new_git_repository_data_form.is_valid():
            git_repository_data = git_repository_models.GitRepositoryData(
                created_by=logged_in_user,
                name=received_new_git_repository_data_form.cleaned_data.get('name'),
                description=received_new_git_repository_data_form.cleaned_data.get('description'),
                url=received_new_git_repository_data_form.cleaned_data.get('url'),
            )
            git_repository_data.save()
            git_repository = git_repository_models.GitRepository.objects.create(
                created_by=logged_in_user,
                current=git_repository_data
            )
            git_repository.save()
            logged_in_user.git_repositories.add(git_repository)
            logged_in_user.save()
            messages.success(request, ('Your git repository was successfully added!'))
            return redirect("git_repository", git_repository_id=git_repository.id)
        else:
            messages.error(request, 'Invalid data received.')
            return redirect("new_git_repository", new_git_repository_form=received_new_git_repository_data_form)

    git_repository_form = new_git_repository_form.NewGitRepositoryDataForm()
    repositories = logged_in_user.git_repositories.all()
    return render(
        request=request,
        template_name="project/git_repository/new_git_repository_template.html",
        context={
            'logged_in_user': logged_in_user,
            'new_git_repository_form': git_repository_form,
            'repositories': repositories
        }
    )
