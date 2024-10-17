from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import user as core_user_models
from frontend.forms.project.project.check_project_label_availability_form import ProjectLabelAvailabilityForm
from project.models import project as project_models


@login_required
def check_project_label_availability(request, label_text=''):
    try:
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=request.user)
    except core_user_models.CoreUser.DoesNotExist:
        return redirect("logout")

    if request.method == "POST":
        project_label_availability_form = ProjectLabelAvailabilityForm(request.POST)
        if project_label_availability_form.is_valid():
            project_label_to_try = project_label_availability_form.cleaned_data.get('label')
            existing_label = project_models.ProjectLabelName.objects.filter(name=project_label_to_try)
            if existing_label.count():
                return render(
                    request=request,
                    template_name="project/project/project_check_project_label_availability.html",
                    context={
                        'available': False,
                    }
                )
            else:
                return render(
                    request=request,
                    template_name="project/project/project_check_project_label_availability.html",
                    context={
                        'available': True,
                    }
                )

    return render(
        request=request,
        template_name="project/project/project_check_project_label_availability.html",
        context={
            'logged_in_user': logged_in_user,
            'available': False,
        }
    )
