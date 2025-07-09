import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from core.models import user as core_user_models
from frontend.forms.project.project import project_form
from project.models import project as project_models


def handle_post(request, logged_in_user, project_id, project):
    received_project_data_form = project_form.ProjectDataForm(request.POST, request.FILES)
    if received_project_data_form.is_valid():
        project_data_form = received_project_data_form.cleaned_data.copy()
        project_label = project_data_form.pop("label")

        if project_label:
            new_project_label_data = project_models.ProjectLabelData.objects.create(
                created_by=logged_in_user,
                label=project_label,
                )
            new_project_label = project_models.ProjectLabel.objects.create(
                created_by=logged_in_user,
                current=new_project_label_data,
                )
            project.label = new_project_label
            # If the project label changed, and it was in the url used to get here, we need to alter the url to give back to the user
            try:
                # But ignore this if the UUID was used
                uuid.UUID(str(project_id))
            except ValueError:
                project_id = project_label

        project_data_form["created_by_id"] = str(logged_in_user.id)
        logged_in_user_project_set = set(logged_in_user.list_projects().values_list('id', flat=True))
        # TODO: Remove these prints
        print("logged_in_user.id:", str(logged_in_user.id))
        print("project.id:", str(project.id))
        print("project_data_form:", project_data_form)
        print("logged_in_user.list_projects().values_list('id', flat=True) before save:", logged_in_user.list_projects().values_list('id', flat=True))
        print("project.users.values_list('id', flat=True) before save:", project.users.values_list('id', flat=True))
        project_data = project_models.ProjectData.objects.create(**project_data_form)
        project.current = project_data
        project.save()  # THIS IS NUKING THE USER'S PROJECT_SET FOR SOME REASON
        print("logged_in_user.list_projects().values_list('id', flat=True) after save:", logged_in_user.list_projects().values_list('id', flat=True))
        print("project.users.values_list('id', flat=True) after save:", project.users.values_list('id', flat=True))
        print("project.id:", str(project.id))
        print("logged_in_user.id:", str(logged_in_user.id))
        logged_in_user.project_set.set(logged_in_user_project_set)
        print("logged_in_user.list_projects().values_list('id', flat=True) after forced setting:", logged_in_user.list_projects().values_list('id', flat=True))

        messages.success(request, ('Your project was successfully updated!'))
    else:
        messages.error(request, 'Error saving project.')

    return redirect("project", project_id=project_id)


@login_required
def project_settings(request, project_id):
    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    try:
        project_uuid = uuid.UUID(str(project_id))
        project = logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        try:
            project = logged_in_user.list_projects().get(label__current__label=project_id)
        except project_models.Project.DoesNotExist:
            messages.error(
                request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
            return redirect("projects")
    except project_models.Project.DoesNotExist:
        messages.error(
            request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    if request.method == "POST":
        return handle_post(request, logged_in_user, project_id, project)

    project_dict = model_to_dict(project.current)
    if project.label:
        project_dict['label'] = project.label.current.label
    form = project_form.ProjectDataForm(project_dict)
    components = project.component_set.all()
    versions = project.version_set.all()
    repositories = project.git_repositories.all()
    users = project.list_users()

    return render(
        request=request,
        template_name="project/project/project_settings_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': project_id,
            'project_form': form,
            'components': components,
            'versions': versions,
            'git_repositories': repositories,
            'users': users,
            }
        )
