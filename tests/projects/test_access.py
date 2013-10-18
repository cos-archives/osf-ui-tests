import httplib as http

from nose.tools import *

from pages.exceptions import HttpError
from pages.project import ProjectPage
from tests.fixtures import ProjectFixture, SubprojectFixture, UserAccessFixture
from tests.components.fixtures import (
    ComponentOfProjectFixture, ComponentOfSubprojectFixture
)


class AccessTests(UserAccessFixture):
    def test_contributor(self):
        self._as_contributor()
        self.page.driver.refresh()

        page = ProjectPage(driver=self.page.driver)

        assert_is_instance(page, ProjectPage)

    def test_non_contributor(self):
        self._as_noncontributor()
        self.page.driver.refresh()

        with assert_raises(HttpError) as cm:
            page = ProjectPage(driver=self.page.driver)
        assert_equal(http.FORBIDDEN, cm.exception.code)

    def test_anonymous(self):
        self._as_anonymous()
        self.page.driver.refresh()

        with assert_raises(HttpError) as cm:
            page = ProjectPage(driver=self.page.driver)
        assert_equal(http.UNAUTHORIZED, cm.exception.code)


class ProjectAccessTestCase(AccessTests, ProjectFixture):
    pass


class SubprojectAccessTestCase(AccessTests, SubprojectFixture):
    pass


class ComponentOfProjectAccessTestCase(AccessTests, ComponentOfProjectFixture):
    pass


class ComponentOfSubprojectAccessTestCase(AccessTests,
                                          ComponentOfSubprojectFixture):
    pass