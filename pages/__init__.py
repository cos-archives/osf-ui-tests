from auth import LoginPage, UserDashboardPage
from project import ProjectPage
from static import HomePage


def _file(category, filename):
    import os
    from collections import namedtuple

    F = namedtuple('File', ('category', 'path', 'name'))

    return F(
        category,
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                'upload_files',
                filename
            )
        ),
        filename
    )


FILES = (
    _file('image', 'test.jpg'),
    _file('image', 'test.gif'),

)