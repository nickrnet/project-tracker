from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import user as core_user_models
from frontend.forms.project.project.check_project_label_availability_form import ProjectLabelAvailabilityForm
from project.models import project as project_models


@login_required
def check_project_label_availability(request):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    if request.method == "POST":
        project_label_availability_form = ProjectLabelAvailabilityForm(request.POST)
        if project_label_availability_form.is_valid():
            project_label_to_try = project_label_availability_form.cleaned_data.get('label')
            existing_label = project_models.ProjectLabelData.active_objects.filter(label=project_label_to_try)
            if existing_label.count():
                return render(
                    request=request,
                    template_name="project/project/project_check_project_label_availability.html",
                    context={
                        'logged_in_user': logged_in_user,
                        'available': False,
                        }
                    )
            else:
                return render(
                    request=request,
                    template_name="project/project/project_check_project_label_availability.html",
                    context={
                        'logged_in_user': logged_in_user,
                        'available': True,
                        }
                    )
        else:
            # Bad data received, say unavailable until fixed
            return render(
                request=request,
                template_name="project/project/project_check_project_label_availability.html",
                context={
                    'logged_in_user': logged_in_user,
                    'available': False,
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
