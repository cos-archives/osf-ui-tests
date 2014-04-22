from nose.tools import *

from tests.forks.fixtures import (
    DeletedProjectForkFixture
)


class Delete(object):
    def test_counter_decremented(self):
        assert_equal(0, self.page.num_forks)

    def test_forks_list(self):
        assert_equal(0, self.page.num_forks)


class ProjectFork(Delete, DeletedProjectForkFixture):
    pass