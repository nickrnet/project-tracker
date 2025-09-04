import uuid

from project.models import project as project_models


def get_project_by_uuid_or_label(logged_in_user, project_id):
    """
    Get a project by its UUID or label.

    Args:
        logged_in_user (CoreUser): A CoreUser object.
        project_id (str): Either the UUID of the project or its label.

    Returns:
        project: The project object if found, otherwise None.
    """

    project = None
    try:
        # Try the project_id as a UUID first
        project_uuid = uuid.UUID(str(project_id))
        project = logged_in_user.list_projects().get(id=project_uuid)
    except ValueError:
        try:
            # Try the project_id as a label
            project = logged_in_user.list_projects().get(label__current__label=project_id)
        except project_models.Project.DoesNotExist:
            project = None
    except project_models.Project.DoesNotExist:
        project = None

    return project
