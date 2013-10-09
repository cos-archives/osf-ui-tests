import datetime as dt

from nose.tools import *

from tests.fixtures import ProjectFixture
from tests.projects.fixtures import ProjectNoDescriptionFixture


class Create(object):

    def test_date_created(self):

        assert_almost_equal(
            self.page.date_created,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )

    def test_title(self):
        assert_equal('Test Project', self.page.title)

    def test_description(self):
        assert_equal('Test Project Description', self.page.description)


class ProjectCreationTests(Create, ProjectFixture):
    pass


class ProjectNoDescriptionCreationTests(Create, ProjectNoDescriptionFixture):
    def test_description(self):
        assert_equal(None, self.page.description)