import unittest

from selenium.common.exceptions import NoSuchElementException

from pages import helpers, LoginPage, ProjectPage


class NodeModifyTests(unittest.TestCase):
    def _test_title(self, page, can_modify=True):
        old_title = page.title
        new_title = "Shiny New Title"

        try:
            page.title = new_title
        except NoSuchElementException:
            if can_modify:
                self.fail('Title editor not found.')

        page.reload()

        self.assertEqual(
            page.title,
            new_title if can_modify else old_title,
        )

        page.close()

    def test_private_project_title_contributor(self):
        self._test_title(
            page=helpers.get_new_project(),
            can_modify=True
        )

    def test_public_project_title_contributor(self):
        page = helpers.get_new_project()
        page.public = True
        self._test_title(page, can_modify=True)

    def test_public_project_title_non_contributor(self):
        page = helpers.get_new_project()
        page.public = True

        _url = page.driver.current_url
        page.close()

        page = LoginPage().log_in(user=helpers.create_user())
        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self._test_title(page, can_modify=False)

    def test_public_project_title_anonymous(self):
        page = helpers.get_new_project()
        page.public = True

        _url = page.driver.current_url

        page.log_out()
        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self._test_title(page, can_modify=False)

    def test_private_subproject_title_contributor(self):
        self._test_title(
            page=helpers.get_new_subproject(),
            can_modify=True
        )

    def test_public_subproject_title_contributor(self):
        page = helpers.get_new_subproject()
        page.public = True
        self._test_title(page, can_modify=True)

    def test_public_subproject_title_non_contributor(self):
        page = helpers.get_new_subproject()
        page.public = True

        _url = page.driver.current_url
        page.close()

        page = LoginPage().log_in(user=helpers.create_user())
        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self._test_title(page, can_modify=False)

    def test_public_subproject_title_anonymous(self):
        page = helpers.get_new_subproject()
        page.public = True

        _url = page.driver.current_url

        page.log_out()
        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self._test_title(page, can_modify=False)
    
    def test_private_component_title_contributor(self):
        self._test_title(
            page=helpers.get_new_component(),
            can_modify=True
        )

    def test_public_component_title_contributor(self):
        page = helpers.get_new_component()
        page.public = True
        self._test_title(page, can_modify=True)

    def test_public_component_title_non_contributor(self):
        page = helpers.get_new_component()
        page.public = True

        _url = page.driver.current_url
        page.close()

        page = LoginPage().log_in(user=helpers.create_user())
        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self._test_title(page, can_modify=False)

    def test_public_component_title_anonymous(self):
        page = helpers.get_new_component()
        page.public = True

        _url = page.driver.current_url

        page.log_out()
        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self._test_title(page, can_modify=False)
    
    def test_private_nested_component_title_contributor(self):
        self._test_title(
            page=helpers.get_new_nested_component(),
            can_modify=True
        )

    def test_public_nested_component_title_contributor(self):
        page = helpers.get_new_nested_component()
        page.public = True
        self._test_title(page, can_modify=True)

    def test_public_nested_component_title_non_contributor(self):
        page = helpers.get_new_nested_component()
        page.public = True

        _url = page.driver.current_url
        page.close()

        page = LoginPage().log_in(user=helpers.create_user())
        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self._test_title(page, can_modify=False)

    def test_public_nested_component_title_anonymous(self):
        page = helpers.get_new_nested_component()
        page.public = True

        _url = page.driver.current_url

        page.log_out()
        page.driver.get(_url)

        page = ProjectPage(driver=page.driver)

        self._test_title(page, can_modify=False)