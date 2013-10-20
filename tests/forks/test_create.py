from nose.tools import *

import pages.project
from tests.forks.fixtures import (
    ForkedComplexProjectFixture,
    ForkedComplexSubprojectFixture,
    ForkedProjectFixture,
    ForkedSubprojectFixture
)


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

    def test_components(self):
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
    """Fork of a clean project"""
    pass


class FromSubproject(Create, ForkedSubprojectFixture):
    """Fork of a clean subproject"""
    pass


class CreateComplex(Create):
    def test_component_links(self):
        """Components of a fork should be copies of the original components"""
        for x, y in zip(self.page.components, self.parent_values['components']):
            assert_not_equal(x  .url, y.url)

    def test_wiki_content(self):
        assert_equal(
            self.parent_values['wiki_content'],
            self.page.get_wiki_content(),
        )


class FromComplexProject(CreateComplex, ForkedComplexProjectFixture):
    pass


class FromComplexSubproject(CreateComplex, ForkedComplexSubprojectFixture):
    pass


class ForkedFrom(object):

    @classmethod
    def setUpClass(cls):
        super(ForkedFrom, cls).setUpClass()
        cls.fork_url = cls.page.driver.current_url
        cls.page.driver.get(cls.page.forked_from_url)
        cls.page = pages.project.ProjectPage(driver=cls.page.driver)

    def test_fork_count(self):
        assert_equal(1, self.page.num_forks)

    def test_fork_listed(self):
        assert_equal(1, len(self.page.forks))

    def test_fork_list_title(self):
        assert_equal(
            'Fork of {}'.format(self.page.title),
            self.page.forks[0].title
        )

    def test_fork_list_url(self):
        assert_equal(
            self.fork_url,
            self.page.forks[0].url
        )


class SourceProjectTestCase(ForkedFrom, ForkedProjectFixture):
    """After forking a project, go back to the original page."""
    pass


class SourceSubprojectTestCase(ForkedFrom, ForkedSubprojectFixture):
    """After forking a subproject, go back to the original page."""
    def test_fork_list_url(self):
        assert_equal(
            self.fork_url,
            self.page.forks.url
        )