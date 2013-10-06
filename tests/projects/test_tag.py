from nose.tools import *

from pages.auth import UserDashboardPage
from pages.auth import UserDashboardPage
from tests.fixtures import ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture, ComponentOfSubprojectFixture
from selenium.common.exceptions import NoSuchElementException


class Tag(object):
    @classmethod
    def setUpClass(cls):
        super(Tag, cls).setUpClass()
        cls.page.add_tag("test tag")

    def test_add_tag(self):
        assert_equal(
            "test tag",
            self.page.driver.find_element_by_css_selector('span.tag span')
            .text.strip(" "),
        )

    def test_delete_tag(self):
        self.page.driver.find_element_by_css_selector('span.tag a').click()
        with self.assertRaises(NoSuchElementException):
            self.page.driver.find_element_by_css_selector('span.tag span')

class ProjectTagTests(Tag, ProjectFixture):
    pass


class SubprojectTagTests(Tag, SubprojectFixture):
    pass


class ComponentOfProjectTagTests(Tag, ComponentOfProjectFixture):
    pass


class ComponentOfSubprojectTagTests(Tag, ComponentOfSubprojectFixture):
    pass
