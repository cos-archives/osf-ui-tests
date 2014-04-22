import httplib as http

from nose.tools import *

from pages.exceptions import HttpError
from pages.project import ProjectPage, FilePage
from tests.fixtures import ProjectFixture, SubprojectFixture, UserAccessFixture
from tests.components.fixtures import ComponentOfProjectFixture, ComponentOfSubprojectFixture
from tests.projects.fixtures import PublicProjectFixture, PublicSubprojectFixture, PublicComponentOfProjectFixture, \
    PublicComponentOfSubprojectFixture, SubprojectOfPublicProjectFixture, ComponentOfPublicProjectFixture, \
    ComponentOfPublicSubprojectFixture, ComponentOfPublicSubprojectOfPublicProjectFixture, FileFixture, \
    ForkAccessFixture, NonContributorModifyFixture


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


class ForkAccessTests(ForkAccessFixture):
    def test_public_subproject_present(self):
        assert_in('Public Subproject', str(self.page.components))

    def test_public_component_present(self):
        assert_in('Public Component', str(self.page.components))

    def test_private_subproject_absent(self):
        assert_not_in('Private Subproject', str(self.page.components))

    def test_private_component_absent(self):
        assert_not_in('Private Component', str(self.page.components))


class ForkProjectAccessTestCase(ForkAccessTests, PublicProjectFixture):
    pass


class ForkSubprojectAccessTestCase(ForkAccessTests, PublicSubprojectFixture):
    pass


class NonContributorModifyTests(NonContributorModifyFixture):
    def test_can_edit_title(self):
        assert_false(self.page.can_edit_title)

    def test_can_access_settings(self):
        assert_false(self.page.can_access_settings)

    def test_can_add_component(self):
        assert_false(self.page.can_add_component)

    def test_can_edit_wiki(self):
        assert_false(self.page.can_edit_wiki)

    def test_can_add_file(self):
        assert_false(self.page.can_add_file)

    def test_can_delete_files(self):
        assert_false(self.page.can_delete_files)

    def test_can_add_contributors(self):
        assert_false(self.page.can_add_contributors)

    def test_can_remove_contributors(self):
        assert_false(self.page.can_remove_contributors)


class PublicProjectNonContributorModify(NonContributorModifyTests, PublicProjectFixture):
    pass


class PublicSubprojectNonContributorModify(NonContributorModifyTests, PublicSubprojectFixture):
    pass
