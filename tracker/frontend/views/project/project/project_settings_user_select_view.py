from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from frontend.util import project as project_utils
from frontend.forms.project.project import project_form
from core.models import user as core_user_models


def handle_post(request, logged_in_user, project):
    selected_user_ids = request.POST.getlist('current_users')
    found_invalid_user = False

    if len(selected_user_ids) > 0:
        users = logged_in_user.list_users().values_list('id', flat=True)
        # Make sure all selected users are valid
        for user_id in selected_user_ids:
            found_valid_user = False
            for user in users:
                if user_id == str(user):
                    found_valid_user = True
                    break
            if found_valid_user:
                continue
            else:
                # Unknown user included in selection, bail as soon as possible
                found_invalid_user = True
                break
    if not found_invalid_user:
        project.update_users(selected_user_ids)
        messages.success(request, 'Project users updated successfully!')
    else:
        messages.error(request, 'Error updating project users.')

    # Get available users (organization members + project users) and exclude
    # any users already assigned to this project.
    available_users = logged_in_user.list_users().exclude(
        pk__in=project.users.values_list('pk', flat=True)
        )
    project_id = str(project.id)
    project_dict = model_to_dict(project.current)
    if project.label:
        project_dict['label'] = str(project.label)
    form = project_form.ProjectDataForm(project_dict)

    return render(
        request=request,
        template_name="project/project/project_settings_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'project_id': project_id,
            'project_form': form,
            'git_repositories': project.git_repositories.all(),
            'available_users': available_users,
            }
        )


@login_required
def user_select(request, project_id):
    """
    Displays the User Select Modal when a user clicks it in the Project Settings modal.
    """

    logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=request.user)

    # Check if user can access project
    project = project_utils.get_project_by_uuid_or_label(logged_in_user, project_id)
    if project is None:
        messages.error(request, 'The specified Project does not exist or you do not have permission to see it. Try to create it, or contact the organization administrator.')
        return redirect("projects")

    if request.method == "POST":
        return handle_post(request, logged_in_user, project)

    # Get available users (organization members + project users) and exclude
    # any users already assigned to this project.
    available_users = logged_in_user.list_users().exclude(
        pk__in=project.users.values_list('pk', flat=True)
        )

    return render(
        request=request,
        template_name="project/project/project_settings_user_select_modal.html",
        context={
            'logged_in_user': logged_in_user,
            'project': project,
            'organization': project.organizationprojects_set.first(),
            'project_users': project.users.all(),
            'available_users': available_users,
            }
        )
