"""
Tests for project logs.
"""

import unittest
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait
from datetime import datetime, timedelta


# Project imports
import base
import util
import config
import uuid

class ProjectLogTests(base.ProjectSmokeTest):

    def _assert_time(self,time_now):
        #assert the time
        time_diff = abs(datetime.utcnow()-time_now)
        self.assertTrue(time_diff < timedelta(minutes=2))


    def test_create_project_log(self):
        """
        test to make sure that creating the project log works correctly

        """
        #get log
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log text
        self.assertEqual(message_log.log_text, self.user_data["fullname"]+ " created project")

        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1]+"/", self.project_url)


    def test_create_node_log(self):
        """
        test to make sure that creating the node log works correctly

        """
        #create a new node
        util.create_node(self.driver)

         #get log
        message_log = self.get_log()

         #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"]+ " created node " + config.node_title)


        #check the user_url
        self.assertEqual(message_log.log_url[0],self.get_user_url())

        #get the node url
        self.driver.find_element_by_css_selector("li span a").click()
        node_url=self.driver.current_url

        #check the node url
        #this part currently failed because something need to be fixed on the webpage
        self.assertEqual(message_log.log_url[2]+"/",node_url)


    def test_project_rename_log(self):
        """
        test to make sure that rename the project log works correctly

        """
        #get user_url
        user_url=self.get_user_url()

        #rename the project
        project_new_name=str(uuid.uuid1())[:6]
        util.project_rename(self.driver, project_new_name)

         #get log
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " changed the title from "
                                               + config.project_title + " to " + project_new_name)


        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], user_url)
        self.assertEqual(message_log.log_url[1]+"/", self.project_url)

        #cleanup
        util.project_rename(self.driver, config.project_title)


    def test_wiki_changes_log(self):
        """
        test to make sure that wiki_changes log works correctly

        """
        # Browse to wiki page
        self.driver.find_element_by_link_text('Wiki').click()


         # Get original version number
        orig_version = util.get_wiki_version(self.driver)

        # edit the wiki
        util.edit_wiki(self.driver)
        util.clear_wiki_text(self.driver)
        util.add_wiki_text(self.driver, str(uuid.uuid1())[:20])
        util.submit_wiki_text(self.driver)

        #get wiki_url
        wiki_url = self.driver.current_url

        #get log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        new_version = str(orig_version + 1)
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " updated wiki page home to version "
                                               + new_version)


        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1], wiki_url)


    def test_add_contributor_log(self):
        """
        test to make sure that add contributor log works correctly

        """
       # Log out
        user_url=self.get_user_url()
        util.logout(self.driver)

        # Create second user and get his url
        second_user_data = util.create_user(self.driver)
        util.login(
            self.driver,
            second_user_data['username'],
            second_user_data['password']
        )
        project_url = util.create_project(self.driver)

        #add contributor
        self.add_contributor(self.user_data)

        #get log
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, second_user_data["fullname"] + " added " + self.user_data['fullname']
                                               + " as contributor on node " + config.project_title)

        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1], user_url)
        self.assertEqual(message_log.log_url[2]+"/", project_url)


    def test_delete_contributor_log(self):
        # Log out
        user_url=self.get_user_url()
        util.logout(self.driver)

        # Create second user and get his url
        second_user_data = util.create_user(self.driver)
        util.login(
            self.driver,
            second_user_data['username'],
            second_user_data['password']
        )
        project_url = util.create_project(self.driver)

        #add contributor
        self.add_contributor(self.user_data)

        #remove contributor
        self.remove_contributor(self.user_data)

         #get log
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, second_user_data["fullname"] + " removed " + self.user_data['fullname']
                                               + " as a contributor from project " + config.project_title)

        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1], user_url)
        self.assertEqual(message_log.log_url[2]+"/", project_url)



# Generate tests
util.generate_tests(ProjectLogTests)

# Run tests
if __name__ == '__main__':
    unittest.main()