from nose.tools import *

import pages.project
from tests.forks.fixtures import ForkedProjectFixture, ForkedSubprojectFixture


class Create(object):
    def test_title(self):
        assert_equal(
            'Fork of {}'.format(self.parent_values['title']),
            self.page.title,
        )

    def test_forked_from(self):
        assert_equal(
            self.parent_values['url'],
            self.page.forked_from_url,
        )

    def test_components_empty(self):
        assert_equal(
            [x.title for x in self.parent_values['components']],
            [x.title for x in self.page.components],
        )

    def test_date_created(self):
        assert_equal(
            self.parent_values['date_created'],
            self.page.date_created
        )

    def test_logs(self):
        assert_equal(
            self.parent_values['logs'],
            self.page.logs[1:],
        )

    def test_fork_action_logged(self):
        assert_in(
            'created fork',
            self.page.logs[0].text,
        )


class FromProject(Create, ForkedProjectFixture):
    pass


class FromSubproject(Create, ForkedSubprojectFixture):
    pass


class ForkedFrom(object):

    @classmethod
    def setUpClass(cls):
        super(ForkedFrom, cls).setUpClass()
        cls.page.driver.get(cls.page.forked_from_url)
        cls.page = pages.project.ProjectPage(driver=cls.page.driver)

    def test_fork_count(self):
        assert_equal(1, self.page.num_forks)


class ForkedFromProjectTestCase(ForkedFrom, ForkedProjectFixture):
    pass