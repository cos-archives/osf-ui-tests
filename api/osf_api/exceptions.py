import httplib as http


class OsfClientException(Exception):
    def __init__(self, *args, **kwargs):
        self.http_status_code = kwargs.get('http_status_code')
        super(OsfClientException, self).__init__(*args)


def assert_auth_passed(r):
    if r.status_code in (http.FORBIDDEN, http.UNAUTHORIZED):
        raise OsfClientException(
            'API call to {} returned HTTP {}'.format(r.url,r.status_code)
        )