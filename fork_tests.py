"""

"""

import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Project imports
from pages import helpers
import base
import util
import config


class ForkTests2(unittest.TestCase):
    """This test case is for testing the act of creating a fork, and consistency
    between a fork and its original node.
    """

    _project = lambda self: helpers.get_new_project()

    def _subproject(self):
        """ Create and return a (sub)project which is the child of a project.

        The ``current_url`` of the driver is the subproject's overview.
        """
        return self._project().add_component(
            title='New Subproject',
            component_type='Project',
        )

    def _test_fork_matches(self, page, attribute):
        """Given a project, fork it and verify that the attribute provided
         matches between the project and its fork.

         Note that the value of the project's attribute is stored before the
         project is forked, as the act of forking may otherwise change the
         state - for example, project's fork should include its log *before*
         the project was forked.
        """
        parent_value = getattr(page, attribute)

        page = page.fork()

        self.assertEqual(
            getattr(page, attribute),
            parent_value,
        )

        page.close()

    def _test_fork_counter_decrement(self, page):
        _url = page.driver.current_url
        num_forks = page.num_forks

        page.fork()
        page.delete()

        page.driver.get(_url)

        self.assertEqual(
            page.num_forks,
            num_forks,
        )

        page.close()

    def test_project_fork_counter_decrement(self):
        self._test_fork_counter_decrement(self._project())

    def test_subproject_fork_counter_decrement(self):
        self._test_fork_counter_decrement(self._subproject())



class ForkTests(base.ProjectSmokeTest):

    def setUp(self):

        # setUp
        super(ForkTests, self).setUp()

    def test_not_fork_a_component(self):
        """
        test to make sure can't fork a component

        """
        #create a component
          # Click New Node button
        self.driver.find_element_by_link_text('Add Component').click()

        # Get form
        form = self.driver.find_element_by_xpath(
        '//form[contains(@action, "newnode")]'
        )

        # Wait for modal to stop moving
        WebDriverWait(self.driver, 3).until(
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[name="title"]')
            )
        )

        # Fill out form
        util.fill_form(
            form,
            {
                'input[name="title"]' : config.node_title,
                '#category' : 'Procedure',
            }
        )

        #check the fork option
        self.driver.find_element_by_css_selector("li span a").click()
        discrib=self.get_element('a[data-original-title="Number of times this node has been forked (copied)"]')\
            .text
        self.assertEqual(discrib, u' 0')

    def tearDown(self):
        # Close WebDriver
        self.driver.close()

# Run tests
if __name__ == '__main__':
    unittest.main()
