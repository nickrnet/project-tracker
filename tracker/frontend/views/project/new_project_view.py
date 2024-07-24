from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.forms.project import new_project_form as new_project_form
from core.models import user as core_user_models
from project.models import project as project_models


@login_required
def new_project(request):
    if request.method == "POST":
        received_new_project_form = new_project_form.NewProjectForm(request.POST, request.FILES)
        if received_new_project_form.is_valid():
            received_new_project_form.save(request=request)
            messages.success(request, ('Your project was successfully added!'))
        else:
            messages.error(request, 'Error saving project.')

        return redirect(reverse("new_project"))

    project_form = new_project_form.NewProjectForm()
    projects = project_models.Project.active_objects.all()
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        logged_in_user = None

    return render(request=request, template_name="project/new_project_template.html", context={'logged_in_user': logged_in_user, 'new_project_form': project_form, 'projects': projects})
