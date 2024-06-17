from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.forms import new_project_form as new_project_form
from project.models import project as project_models


@login_required
def new_project(request):
    if request.method == "POST":
        received_new_project_form = new_project_form.NewProjectForm(request.POST, request.FILES)
        if received_new_project_form.is_valid():
            received_new_project_form.save(request=request)
            messages.success(request, ('Your git repository was successfully added!'))
        else:
            messages.error(request, 'Error saving git repository.')

        return redirect(reverse("new_project"))

    project_form = new_project_form.NewProjectForm()
    projects = project_models.Project.active_objects.all()

    return render(request=request, template_name="new_project_template.html", context={'new_project_form': project_form, 'projects': projects})
