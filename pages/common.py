from collections import namedtuple

User = namedtuple('User', ['full_name', 'email', 'password'])


class User(object):
    full_name = None
    email = None
    password = None
    id = None

    def __init__(
        self,
        full_name=None,
        email=None,
        password=None,
        profile_url=None,
    ):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.profile_url = profile_url

        if profile_url:
            self.id = profile_url.rstrip('/').split('/')[-1]

    def __eq__(selfm):