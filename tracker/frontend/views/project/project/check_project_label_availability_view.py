from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.models import user as core_user_models
from frontend.forms.project.project.check_project_label_availability_form import ProjectLabelAvailabilityForm
from project.models import project as project_models


class CheckProjectLabelAvailabilityView(LoginRequiredMixin, View):
    def get(self, request):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
        return render(
            request=request,
            template_name="project/project/project_check_project_label_availability.html",
            context={
                'logged_in_user': logged_in_user,
                'available': False,
                }
            )

    def post(self, request):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)
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
