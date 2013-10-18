import httplib as http

from nose.tools import *

from pages.exceptions import HttpError
from pages.project import ProjectPage
from tests.fixtures import ProjectFixture, SubprojectFixture, UserAccessFixture
from tests.components.fixtures import (
    ComponentOfProjectFixture, ComponentOfSubprojectFixture
)


class PublicProjectFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicProjectFixture, cls).setUpClass()
        cls.page.public = True


class PublicSubprojectFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicSubprojectFixture, cls).setUpClass()
        cls.page.public = True


class PublicComponentOfProjectFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicComponentOfProjectFixture, cls).setUpClass()
        cls.page.public = True


class PublicComponentOfSubprojectFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicComponentOfSubprojectFixture, cls).setUpClass()
        cls.page.public = True


class DefaultAccessTests(UserAccessFixture):
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


class PublicAccessTests(DefaultAccessTests):
    def test_non_contributor(self):
        self._as_noncontributor()
        self.page.driver.refresh()

        page = ProjectPage(driver=self.page.driver)

        assert_is_instance(page, ProjectPage)

    def test_anonymous(self):
        self._as_anonymous()
        self.page.driver.refresh()

        page = ProjectPage(driver=self.page.driver)

        assert_is_instance(page, ProjectPage)


class ProjectAccessTestCase(DefaultAccessTests, ProjectFixture):
    pass


class SubprojectAccessTestCase(DefaultAccessTests, SubprojectFixture):
    pass


class ComponentOfProjectAccessTestCase(DefaultAccessTests, ComponentOfProjectFixture):
    pass


class ComponentOfSubprojectAccessTestCase(DefaultAccessTests,
                                          ComponentOfSubprojectFixture):
    pass


class PublicProjectAccessTestCase(PublicAccessTests, PublicProjectFixture):
    pass


class PublicSubprojectAccessTestCase(PublicAccessTests, PublicSubprojectFixture):
    pass


class PublicComponentOfProjectAccessTestCase(PublicAccessTests,
                                             PublicComponentOfProjectFixture):
    pass


class PublicComponentOfSubprojectAccessTestCase(PublicAccessTests,
                                                PublicComponentOfSubprojectFixture):
    pass