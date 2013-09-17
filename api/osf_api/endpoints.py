import config


def add_project(parent=None):
    """Builds the endpoint for adding a project."""
    if parent:
        # If this is a subproject, hit the parent's newnode endpoint
        return add_node(parent)

    # else, use the user's endpoint
    return '{}/project/new'.format(config.osf_home)


def add_node(parent):
    """Builds the endpoint for adding a component to a project"""
    return '{}/project/{}/newnode'.format(
        config.osf_home,
        parent.id
    )