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

class CreateForkTests(base.ProjectSmokeTest):

    def setUp(self):

        # 
        super(CreateForkTests, self).setUp()

        # go to the project
        self.url = util.goto_project(self.driver)

        # Make the project public
        util.make_project_public(self.driver, self.url)

        time.sleep(3)
        
        # add to the wiki
        self.driver.find_element_by_link_text('Wiki').click()
        util.edit_wiki(self.driver)
        util.add_wiki_text(
            self.driver, "This is wiki test")
        util.submit_wiki_text(self.driver)
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


    def test_create_fork(self):

        #go to the project that is now public
        self.driver.get(self.url)
        time.sleep(2)
        link = self.driver.find_element_by_xpath(
            '//a[@class="btn"][@data-original-title="Number of times this node has been forked (copied)"]')
        link.click()
        time.sleep(2)
        title = self.driver.find_element_by_css_selector("h1#node-title-editable").text
        self.assertEqual(title,
            "Fork of test project")
        wiki_text = util.get_wiki_text(self.driver)
        self.assertEqual(self.wiki_text, wiki_text)


    def tearDown(self):

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
        util.logout(self.driver)

        # Close WebDriver
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
