import config
import unittest
import util

from base import ProjectSmokeTest, not_implemented
from pages import helpers
from pages.auth import LoginPage
from pages.project import NodePage, ProjectPage
from pages.exceptions import PageException

from selenium.common.exceptions import TimeoutException


class ProjectSecurityTests2(unittest.TestCase):
    def _test_add_contributor_listed(self, page):
        second_user = helpers.create_user()

        page.add_contributor(second_user)

        self.assertIn(
            second_user.full_name,
            [x.full_name for x in page.contributors]
        )

        page.close()

    def test_project_add_contributors_listed(self):
        self._test_add_contributor_listed(helpers.get_new_project())

    def test_subproject_add_contributors_listed(self):
        self._test_add_contributor_listed(helpers.get_new_subproject())

    def test_component_add_contributors_listed(self):
        self._test_add_contributor_listed(helpers.get_new_component())

    def test_nested_component_add_contributors_listed(self):
        self._test_add_contributor_listed(helpers.get_new_nested_component())

    def _test_add_contributor_access(self, page):
        _url = page.driver.current_url
        second_user = helpers.create_user()

        page.add_contributor(second_user)

        self.assertIn(
            second_user.full_name,
            [x.full_name for x in page.contributors]
        )

        page.close()

        page = LoginPage()
        page.log_in(second_user)

        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self.assertIn(
            second_user.full_name,
            [x.full_name for x in page.contributors],
        )

        page.close()

    def test_project_add_contributors_access(self):
        self._test_add_contributor_access(helpers.get_new_project())

    def test_subproject_add_contributors_access(self):
        self._test_add_contributor_access(helpers.get_new_subproject())

    def test_component_add_contributors_access(self):
        self._test_add_contributor_access(helpers.get_new_component())

    def test_nested_component_add_contributors_access(self):
        self._test_add_contributor_access(helpers.get_new_nested_component())

    def _test_can_access(self, page, user=None, can_access=True):
        _url = page.driver.current_url
        _id = page.id

        page.close()

        if user:
            page = LoginPage().log_in(user)
            page.driver.get(_url)

            assertion = self.assertTrue if can_access else self.assertFalse

            # verify that we weren't redirected
            assertion(
                page.driver.current_url == _url
            )

            page.close()
        else:
            if can_access:
                page = NodePage(url=_url)
                page.close()
            else:
                with self.assertRaises(PageException):
                    ProjectPage(id=_id)

    def test_private_project_contributor_access(self):
        page = helpers.get_new_project()
        user = helpers.create_user()

        page.add_contributor(user)

        self._test_can_access(page, user)

    def test_private_project_non_contributor_access(self):
        page = helpers.get_new_project()
        user = helpers.create_user()

        self._test_can_access(page, user, False)

    def test_private_project_anonymous_access(self):
        page = helpers.get_new_project()

        self._test_can_access(page, can_access=False)

    def test_public_project_contributor_access(self):
        page = helpers.get_new_project()
        user = helpers.create_user()
        page.public = True

        page.add_contributor(user)

        self._test_can_access(page, user)

    def test_public_project_non_contributor_access(self):
        page = helpers.get_new_project()
        user = helpers.create_user()
        page.public = True

        self._test_can_access(page, user)

    def test_public_project_anonymous_access(self):
        page = helpers.get_new_project()
        page.public = True

        self._test_can_access(page)

    def test_private_subproject_contributor_access(self):
        page = helpers.get_new_subproject()
        user = helpers.create_user()

        page.add_contributor(user)

        self._test_can_access(page, user)

    def test_private_subproject_non_contributor_access(self):
        page = helpers.get_new_subproject()
        user = helpers.create_user()

        self._test_can_access(page, user, False)

    def test_private_subproject_anonymous_access(self):
        page = helpers.get_new_subproject()

        self._test_can_access(page, can_access=False)

    def test_public_subproject_contributor_access(self):
        page = helpers.get_new_subproject()
        user = helpers.create_user()
        page.public = True

        page.add_contributor(user)

        self._test_can_access(page, user)

    def test_public_subproject_non_contributor_access(self):
        page = helpers.get_new_subproject()
        user = helpers.create_user()
        page.public = True

        self._test_can_access(page, user)

    def test_public_subproject_anonymous_access(self):
        page = helpers.get_new_subproject()
        page.public = True

        self._test_can_access(page)

    def test_private_component_contributor_access(self):
        page = helpers.get_new_component()
        user = helpers.create_user()

        page.add_contributor(user)

        self._test_can_access(page, user)

    def test_private_component_non_contributor_access(self):
        page = helpers.get_new_component()
        user = helpers.create_user()

        self._test_can_access(page, user, False)

    def test_private_component_anonymous_access(self):
        page = helpers.get_new_component()

        self._test_can_access(page, can_access=False)

    def test_public_component_contributor_access(self):
        page = helpers.get_new_component()
        user = helpers.create_user()
        page.public = True

        page.add_contributor(user)

        self._test_can_access(page, user)

    def test_public_component_non_contributor_access(self):
        page = helpers.get_new_component()
        user = helpers.create_user()
        page.public = True

        self._test_can_access(page, user)

    def test_public_component_anonymous_access(self):
        page = helpers.get_new_component()
        page.public = True

        self._test_can_access(page)

    def test_private_nested_component_contributor_access(self):
        page = helpers.get_new_nested_component()
        user = helpers.create_user()

        page.add_contributor(user)

        self._test_can_access(page, user)

    def test_private_nested_component_non_contributor_access(self):
        page = helpers.get_new_nested_component()
        user = helpers.create_user()

        self._test_can_access(page, user, False)

    def test_private_nested_component_anonymous_access(self):
        page = helpers.get_new_nested_component()

        self._test_can_access(page, can_access=False)

    def test_public_nested_component_contributor_access(self):
        page = helpers.get_new_nested_component()
        user = helpers.create_user()
        page.public = True

        page.add_contributor(user)

        self._test_can_access(page, user)

    def test_public_nested_component_non_contributor_access(self):
        page = helpers.get_new_nested_component()
        user = helpers.create_user()
        page.public = True

        self._test_can_access(page, user)

    def test_public_nested_component_anonymous_access(self):
        page = helpers.get_new_nested_component()
        page.public = True

        self._test_can_access(page)


class ProjectSecurityTest(ProjectSmokeTest):

    def setUp(self):
        super(ProjectSecurityTest, self).setUp()

        self.second_user = self.create_user()

    def test_remove_contributor(self):

        # Add a contributor
        self.goto('dashboard')
        self.add_contributor(self.second_user)

        # refresh the page
        self.goto('dashboard')

        # remove the contributor
        self.remove_contributor(self.second_user)

        # log out and back in as the second user
        self.log_out()
        self.log_in(self.second_user)

        self.goto('dashboard')

        # There should be no project list, so just make sure the project title
        # isn't on the page.
        self.assertTrue(
            'not authorized' in self.get_element('div.alert').text
        )

        # log out and back in as the first user, so teardown will work
        self.log_out()
        self.log_in(self.user_data)

    def test_public_non_contributor_modify(self):
        """ Users who are not contributors should not have access to the wiki
        edit page of a public project.
        """

        self.make_public()

        second_user = self.create_user()

        self.log_out()
        self.log_in(second_user)

        # Try to edit the wiki
        self.goto('wiki')
        self.driver.get('/'.join([
            self.driver.current_url.strip('/'),
            'edit',
        ]))

        # should have redirect the user elsewhere
        self.assertNotIn(
            'edit',
            self.driver.current_url
        )

        # try to add a node
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.add_component('hypothesis', 'foo')

        # try to delete the project
        self.goto('settings')
        self.assertNotIn(
            'settings',
            self.driver.current_url
        )

        # try to rename the project
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.edit_title('foo')

        # try to add a contributor
        self.goto('dashboard')
        with self.assertRaises(TimeoutException):
            self.add_contributor(second_user)

        # try to remove a contributor
        self.goto('dashboard')
        # with self.assertRaises(TimeoutException):
        self.remove_contributor(self.user_data)
        self.goto('dashboard')
        self.assertIn(
            self.user_data['fullname'],
            self.get_element('#contributors').text,
        )

        # log back in so teardown works.
        self.log_out()
        self.log_in()

    @not_implemented
    def test_fork_with_private_components(self):
        raise NotImplementedError
