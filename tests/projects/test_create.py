import datetime as dt

from nose.tools import *

from pages.exceptions import PageException
from tests.fixtures import ProjectFixture, UserFixture
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

    def test_forkable(self):
        assert_true(self.page.forkable)


class CreationTests(Create, ProjectFixture):
    pass


class CreateNoDescriptionTests(Create, ProjectNoDescriptionFixture):
    def test_description(self):
        assert_equal(None, self.page.description)


class CreateNoTitleTests(UserFixture):
    """This test case changes state"""
    def test_create_no_title(self):
        """ Create a project with no title.

        User shouldn't be able to do this, but attempting it results in a 500,
        and the correct behavior is not yet defined.
        """
        with assert_raises(PageException):
            self.page = self.page.new_project(title='')

        assert_in(
            'Title is required',
            self.page.driver.find_element_by_css_selector('div.alert').text
        )