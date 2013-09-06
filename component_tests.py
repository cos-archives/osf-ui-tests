import unittest

from pages import helpers


class ComponentTests(unittest.TestCase):

    def _test_backlink_to_parent(self, component_type):
        page = helpers.get_new_project('New Project')
        parent_project_url = page.driver.current_url

        page = page.add_component(title='New Component')

        self.assertEqual(
            page.parent_link,
            parent_project_url,
        )

    def test_component_backlink_to_parent(self):
        self._test_backlink_to_parent(component_type='Other')

    def test_project_backlink_to_parent(self):
        self._test_backlink_to_parent(component_type='Project')