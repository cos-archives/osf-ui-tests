import unittest

from selenium.webdriver import ActionChains

from base import ProjectSmokeTest


class ComponentAccessCase(ProjectSmokeTest):

    @unittest.skip('Fails due to Selenium troubles')
    def test_reorder_components(self):
        self.add_component('hypothesis', 'first')
        self.add_component('hypothesis', 'second')

        self.driver.get(self.project_url)

        # Second method: by element
        ac = ActionChains(self.driver)
        a = self.driver.find_element_by_css_selector('#Nodes li:first-child')
        b = self.driver.find_element_by_css_selector('#Nodes li:last-child')
        ac.drag_and_drop(a, b).perform()

        self.driver.get(self.project_url)
        self.assertEqual(
            self.get_element('#Nodes li:first-child').text,
            'second',
        )
