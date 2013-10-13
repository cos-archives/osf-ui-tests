"""
Tests for project logs.
"""

import time
import unittest
from selenium.webdriver.common.action_chains import ActionChains

# Project imports
import base
import util
import config
import uuid


class ProjectLogTests(base.ProjectSmokeTest):

    def test_wiki_changes_log(self):
        """
        test to make sure that wiki_changes log works correctly
        """

        # Browse to wiki page
        self.driver.find_element_by_link_text('Wiki').click()

        # Get original version number
        orig_version = util.get_wiki_version(self.driver)

        # edit the wiki
        self._add_wiki(str(uuid.uuid1())[:20])

        #get wiki_url
        wiki_url = self.driver.current_url

        #get log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        new_version = str(orig_version + 1)
        self.assertEqual(
            message_log.log_text,
            u'{} updated wiki page home to version {}'.format(
                self.user_data["fullname"],
                new_version,
            )
        )

        #check the user_url and project_url
        self.assertEqual(
            message_log.log_url[0],
            self.get_user_url()
        )
        self.assertEqual(
            message_log.log_url[1],
            wiki_url
        )

    def test_delete_contributor_log(self):
        # As of 9 Sep 2013, the log says "component"; expected "project"

        # Log out
        user_url = self.get_user_url()
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
        self.assertEqual(
            message_log.log_text,
            u'{} removed {} as a contributor from project {}'.format(
                second_user_data["fullname"],
                self.user_data['fullname'],
                config.project_title
            )
        )

        #check the second user_url, first user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1], user_url)
        self.assertEqual(message_log.log_url[2], project_url)