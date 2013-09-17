import config
root = config.osf_home

def add_project(parent=None):
    """Builds the endpoint for adding a project."""
    if parent:
        # If this is a subproject, hit the parent's newnode endpoint
        return add_component(parent)

    # else, use the user's endpoint
    return '{}/project/new'.format(config.osf_home)


def add_component(parent):
    """Builds the endpoint for adding a component to a project"""
    return '{}/project/{}/newnode'.format(
        config.osf_home,
        parent.id
    )


def edit_project(project_id):
    """Builds the endpoint for editing an existing project"""
    return '{}/project/{}/edit'.format(
        config.osf_home,
        project_id
    )


def edit_component(component_id, project_id):
    """Builds the endpoint for editing an existing component"""
    return '{}/project/{}/node/{}/edit'.format(
        config.osf_home,
        project_id,
        component_id,
    )