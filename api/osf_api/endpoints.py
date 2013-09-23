import config
root = config.osf_home

# Nodes

def add_node(parent_id=None):
    """Builds the endpoint for adding a component to a project"""
    if parent_id:
        return '{}/project/{}/newnode'.format(
            config.osf_home,
            parent_id
        )
    else:
        return '{}/project/new'.format(config.osf_home)


def add_node_api_key(node_id, parent_id=None):
    return '{}/api/v1/project/{}/create_key/'.format(
        root,
        '{}/node/{}'.format(
            parent_id, node_id) if parent_id else node_id,
    )


def get_node(node_id, parent_id=None):
    return '{}/api/v1/project/{}/get_summary/'.format(
        root,
        '{}/node/{}'.format(
            parent_id, node_id) if parent_id else node_id,
    )


def get_node_api_keys(node_id, parent_id=None):
    return '{}/api/v1/project/{}/keys/'.format(
        root,
        '{}/node/{}'.format(
            parent_id, node_id) if parent_id else node_id,
    )


def edit_node(node_id, parent_id=None):
    """Builds the endpoint for editing an existing component"""
    return '{}/api/v1/project/{}/edit/'.format(
        config.osf_home,
        '{}/node/{}'.format(
            parent_id, node_id) if parent_id else node_id,
    )


# Users


def get_user(user_id=None):
    if user_id:
        return '{}/api/v1/profile/{}/'.format(root, user_id)
    return '{}/api/v1/profile/'.format(root)


def get_user_public_projects(user_id):
    return '{}/api/v1/profile/{}/public_projects'.format(root, user_id)