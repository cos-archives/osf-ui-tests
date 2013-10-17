from nose.tools import *

from tests.fixtures import ProjectFixture, SubprojectFixture

from tests.components.fixtures import ComponentOfProjectFixture, ComponentOfSubprojectFixture


class WatchFixture(object):
    @classmethod
    def setUpClass(cls):
        super(WatchFixture, cls).setUpClass()
        cls.first_log = cls.page.logs[0]
        cls.old_watchers = cls.page.num_watchers
        cls.page.watched = True

class WatchTests(WatchFixture):
    def test_watched(self):
        assert_true(self.page.watched)

    def test_watchers(self):
        assert_equal(
            self.old_watchers + 1,
            self.page.num_watchers,
        )

    def test_logs(self):
        assert_true(self.first_log in self.page.logs)


class WatchProjectTestCase(WatchTests, ProjectFixture):
    pass


class WatchSubprojectTestCase(WatchTests, SubprojectFixture):
    pass


class WatchComponentOfProjectTestCase(WatchTests, ComponentOfProjectFixture):
    pass


class WatchComponentOfSubprojectTestCase(WatchTests, ComponentOfSubprojectFixture):
    pass


class UnwatchTests(WatchFixture):
    @classmethod
    def setUpClass(cls):
        super(UnwatchTests, cls).setUpClass()
        cls.old_watchers = cls.page.num_watchers
        cls.page.watched = False

    def test_watched(self):
        assert_false(self.page.watched)

    def test_watchers(self):
        assert_equal(
            self.old_watchers - 1,
            self.page.num_watchers,
        )

class UnwatchProjectTestCase(UnwatchTests, ProjectFixture):
    pass


class UnwatchSubprojectTestCase(UnwatchTests, SubprojectFixture):
    pass


class UnwatchComponentOfProjectTestCase(UnwatchTests, ComponentOfProjectFixture):
    pass


class UnwatchComponentOfSubprojectTestCase(UnwatchTests, ComponentOfSubprojectFixture):
    pass