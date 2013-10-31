import httplib as http

from nose.tools import *

from pages import FILES
from pages.exceptions import HttpError
from pages.project import ProjectPage, FilePage
from tests.fixtures import ProjectFixture, SubprojectFixture, UserAccessFixture
from tests.components.fixtures import (
    ComponentOfProjectFixture, ComponentOfSubprojectFixture, ComponentFixture
)


class PublicProjectFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicProjectFixture, cls).setUpClass()
        cls.page.public = True


class PublicSubprojectFixture(SubprojectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicSubprojectFixture, cls).setUpClass()
        cls.page.public = True


class PublicComponentOfProjectFixture(ComponentOfProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicComponentOfProjectFixture, cls).setUpClass()
        cls.page.public = True


class PublicComponentOfSubprojectFixture(ComponentOfSubprojectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicComponentOfSubprojectFixture, cls).setUpClass()
        cls.page.public = True


class SubprojectOfPublicProjectFixture(PublicProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(SubprojectOfPublicProjectFixture, cls).setUpClass()
        cls.page = cls.page.add_component(
            title='Test Subproject',
            component_type='Project',
        )


class PublicSubprojectOfPublicProjectFixture(SubprojectOfPublicProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicSubprojectOfPublicProjectFixture, cls).setUpClass()
        cls.page.public = True


class ComponentOfPublicProjectFixture(ComponentFixture, PublicProjectFixture):
    pass


class ComponentOfPublicSubprojectFixture(ComponentFixture, PublicSubprojectFixture):
    pass


class ComponentOfPublicSubprojectOfPublicProjectFixture(ComponentFixture, PublicSubprojectOfPublicProjectFixture):
    pass


class PrivateAccessTests(UserAccessFixture):
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


class PublicAccessTests(PrivateAccessTests):
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


class PrivateProjectAccessTestCase(PrivateAccessTests, ProjectFixture):
    """Test access to a private project"""
    pass


class PrivateSubprojectAccessTestCase(PrivateAccessTests, SubprojectFixture):
    """Test access to a private subproject of a private project"""
    pass


class PrivateComponentOfProjectAccessTestCase(PrivateAccessTests, ComponentOfProjectFixture):
    """Test access to a private component of a private project"""
    pass


class PrivateComponentOfSubprojectAccessTestCase(PrivateAccessTests,
                                          ComponentOfSubprojectFixture):
    """Test access to a private component of a private subproject of a private project"""
    pass


class PublicProjectAccessTestCase(PublicAccessTests, PublicProjectFixture):
    """Test access to a public project"""
    pass


class PublicSubprojectAccessTestCase(PublicAccessTests, PublicSubprojectFixture):
    """Test access to a public subproject of a private project"""
    pass


class PublicComponentOfProjectAccessTestCase(PublicAccessTests,
                                             PublicComponentOfProjectFixture):
    """Test access to a public component of a private project"""
    pass


class PublicComponentOfSubprojectAccessTestCase(PublicAccessTests,
                                                PublicComponentOfSubprojectFixture):
    """Test access to a public component of a private subproject of a private project"""
    pass


class PrivateSubprojectOfPublicProjectTestCase(PrivateAccessTests, SubprojectOfPublicProjectFixture):
    """Test access to a private subproject of a public project"""
    pass


class PrivateComponentOfPublicProjectTestCase(PrivateAccessTests, ComponentOfPublicProjectFixture):
    """Test access to a private component of a public project"""
    pass


class PrivateComponentOfPublicSubprojectTestCase(PrivateAccessTests, ComponentOfPublicSubprojectFixture):
    """Test access to a private component of a public subproject of a private project"""
    pass


class PrivateComponentOfPublicSubprojectOfPublicProjectTestCase(PrivateAccessTests,
                                                                ComponentOfPublicSubprojectOfPublicProjectFixture):
    """Test access to a private component of a public subproject of a public project"""
    pass


class FileFixture(object):
    @classmethod
    def setUpClass(cls):
        super(FileFixture, cls).setUpClass()

        cls.page.add_file([x for x in FILES if x.name == 'test.jpg'][0])
        cls.file_url = '{}{}'.format(cls.page.driver.current_url, 'test.jpg')
        cls.page.driver.get(cls.file_url)


class PrivateFileAccessTests(UserAccessFixture):
    def test_contributor(self):
        self._as_contributor()
        self.page.driver.refresh()

        page = FilePage(driver=self.page.driver)

        assert_is_instance(page, FilePage)

    def test_non_contributor(self):
        self._as_noncontributor()
        self.page.driver.refresh()

        with assert_raises(HttpError) as cm:
            page = FilePage(driver=self.page.driver)
        assert_equal(http.FORBIDDEN, cm.exception.code)

    def test_anonymous(self):
        self._as_anonymous()
        self.page.driver.refresh()

        with assert_raises(HttpError) as cm:
            page = FilePage(driver=self.page.driver)
        assert_equal(http.UNAUTHORIZED, cm.exception.code)


class FileOfProjectTestCase(PrivateFileAccessTests, FileFixture, ProjectFixture):
    """Test access to files of a private project"""
    pass


class FileOfSubprojectOfPublicProjectTestCase(PrivateFileAccessTests, FileFixture, SubprojectOfPublicProjectFixture):
    """Test access to files of a private subproject of a public project"""
    pass


class FileOfComponentOfPublicProjectTestCase(PrivateFileAccessTests, FileFixture, ComponentOfPublicProjectFixture):
    """Test access to files of a private component of a public project"""
    pass


class FileOfComponentOfPublicSubprojectTestCase(PrivateFileAccessTests, FileFixture,
                                                ComponentOfPublicSubprojectFixture):
    """Test access to files of a private component of a public subproject of a private project"""
    pass


class FileOfComponentOfPublicSubprojectOfPublicProjectTestCase(PrivateFileAccessTests, FileFixture,
                                                               ComponentOfPublicSubprojectOfPublicProjectFixture):
    """Test access to files of a private component of a public subproject of a public project"""
    pass