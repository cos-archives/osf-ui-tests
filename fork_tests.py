"""

"""

import unittest
import time

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Project imports
import base
import util
import config

class ForkTests(base.ProjectSmokeTest):

    def setUp(self):

        # setUp
        super(ForkTests, self).setUp()



    def test_create_fork(self):
        """
        test to make sure a fork is created

        """
        # Make the project public
        util.make_project_public(self.driver, self.project_url)


        # add to the wiki
        self.get_element('div.subnav li a')
        self.driver.find_element_by_link_text('Wiki').click()
        self._add_wiki("This is wiki test")
        self.wiki_text = util.get_wiki_text(self.driver)

        #logout
        util.logout(self.driver)

        self.second_user_data = util.create_user(self.driver)

        # Login to test account
        util.login(
            self.driver,
            self.second_user_data['username'],
            self.second_user_data['password']
        )

        #go to the project that is now public
        self.driver.get(self.project_url)
        self.get_element(
            'a[data-original-title="Number of times this node has been forked (copied)"]').click()
        title = self.get_element("h1#node-title-editable").text
        self.assertEqual(title,
            "Fork of test project")
        wiki_text = util.get_wiki_text(self.driver)
        self.assertEqual(self.wiki_text, wiki_text)

        # Delete test project
        util.login(self.driver,
            self.user_data['username'],
            self.user_data['password'],
        )
        util.delete_project(self.driver)
        util.logout(self.driver)

        util.login(self.driver,
            self.second_user_data['username'],
            self.second_user_data['password'],
        )
        util.delete_project(self.driver, "Fork of test project")


    def test_fork_link_to_origin_tests(self):
        """
        test to make sure a fork links to original project

        """
        #fork a project
        self.get_element(
            'a[data-original-title="Number of times this node has been forked (copied)"]').click()

        #click the link to original project
        self.driver.find_element_by_css_selector("header#overview.jumbotron.subhead p#contributors")\
            .find_element_by_xpath('a[contains(.,"/project/")]').click()

        #check the url and project title
        title = self.get_element("h1#node-title-editable").text
        self.assertEqual(title, config.project_title)
        self.assertEqual(self.driver.current_url, self.project_url)

        #cleanup
        util.delete_project(self.driver)
        util.delete_project(self.driver, "Fork of test project")


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
        util.wait_until_stable(
            self.driver.find_element_by_css_selector(
                'input[name="title"]'
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

        #cleanup
        util.delete_project(self.driver)


    def test_fork_nested_project(self):
        """
        test to make sure can fork nested project

        """
        util.create_node(self.driver)

         #fork the project and check the node
        self.get_element(
            'a[data-original-title="Number of times this node has been forked (copied)"]').click()
        self.driver.find_element_by_css_selector("li span a").click()
        title = self.get_element("h1#node-title-editable").text
        self.assertEqual(title, config.node_title)


        #cleanup
        util.delete_project(self.driver, "Fork of " + config.project_title)
        util.delete_project(self.driver)

    def tearDown(self):

        util.logout(self.driver)

        # Close WebDriver
        self.driver.close()

# Generate tests
util.generate_tests(ForkTests)

# Run tests
if __name__ == '__main__':
    unittest.main()
