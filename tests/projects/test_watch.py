from nose.tools import *

from tests.fixtures import ProjectFixture, SubprojectFixture

from tests.components.fixtures import ComponentOfProjectFixture, ComponentOfSubprojectFixture


class WatchFixture(object):
    @classmethod
    def setUpClass(cls):
        super(WatchFixture, cls).setUpClass()
        cls.node_logs = cls.page.logs
        cls.old_num_watchers = cls.page.num_watchers
        cls.page.watched = True


class UnwatchFixture(WatchFixture):
    @classmethod
    def setUpClass(cls):
        super(UnwatchFixture, cls).setUpClass()
        cls.old_num_watchers = cls.page.num_watchers
        cls.page.watched = False


class WatchTests(WatchFixture):
    def test_watched(self):
        assert_true(self.page.watched)

    def test_watchers(self):
        assert_equal(
            self.old_num_watchers + 1,
            self.page.num_watchers,
        )


class WatchProjectTestCase(WatchTests, ProjectFixture):
    pass


class WatchSubprojectTestCase(WatchTests, SubprojectFixture):
    pass


class WatchComponentOfProjectTestCase(WatchTests, ComponentOfProjectFixture):
    pass


class WatchComponentOfSubprojectTestCase(WatchTests, ComponentOfSubprojectFixture):
    pass


class UnwatchTests(UnwatchFixture):

    def test_watched(self):
        assert_false(self.page.watched)

    def test_watchers(self):
        assert_equal(
            self.old_num_watchers - 1,
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


class WatchLogTests(WatchFixture):
    @classmethod
    def setUpClass(cls):
        super(WatchLogTests, cls).setUpClass()
        cls.page = cls.page.user_dashboard

    def test_logs(self):
        for log in self.node_logs:
            assert_true(log in self.page.watch_logs)


class WatchLogProjectTestCase(WatchLogTests, ProjectFixture):
    pass


class WatchLogSubprojectTestCase(WatchLogTests, SubprojectFixture):
    pass


class WatchLogComponentOfProjectTestCase(WatchLogTests, ComponentOfProjectFixture):
    pass


class WatchLogComponentOfSubprojectTestCase(WatchLogTests, ComponentOfSubprojectFixture):
    pass


class UnwatchLogTests(UnwatchFixture):
    @classmethod
    def setUpClass(cls):
        super(UnwatchLogTests, cls).setUpClass()
        cls.page = cls.page.user_dashboard

    def test_logs(self):
        for log in self.node_logs:
            assert_false(log in self.page.watch_logs)


class UnwatchLogProjectTestCase(UnwatchLogTests, ProjectFixture):
    pass


class UnwatchLogSubprojectTestCase(UnwatchLogTests, SubprojectFixture):
    pass


class UnwatchLogComponentOfProjectTestCase(UnwatchLogTests, ComponentOfProjectFixture):
    pass


class UnwatchLogComponentOfSubprojectTestCase(UnwatchLogTests, ComponentOfSubprojectFixture):
    pass