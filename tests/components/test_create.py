import datetime as dt

from nose import SkipTest
from nose.tools import *

from tests.components.fixtures import (
    ComponentOfProjectFixture,
    ComponentOfSubprojectFixture,
)


class Create(object):

    def test_date_created(self):

        assert_almost_equal(
            self.page.date_created,
            dt.datetime.now(),
            delta=dt.timedelta(minutes=2)
        )

    def test_title(self):
        assert_equal('Test Component', self.page.title)

    def test_link_to_parent(self):
        assert_equal(
            self.parent_values['url'],
            self.page.parent_link,
        )

    def test_forkable(self):
        assert_false(self.page.forkable)

    def test_logged(self):
        assert_equal(
            u'{} created component {}'.format(
                self.users[0].full_name,
                self.page.title,
            ),
            self.page.logs[0].text
        )


class ComponentOfProjectCreationTests(Create, ComponentOfProjectFixture):
    pass


class ComponentOfSubprojectCreationTests(Create, ComponentOfSubprojectFixture):
    pass