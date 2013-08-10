"""
Tests for project logs on node actions.
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
import os
import shutil

class NodeLogTests(base.ProjectSmokeTest):

    def setUp(self):

        super(NodeLogTests, self).setUp()

        #create a new node
        util.create_node(self.driver)
        self.driver.find_element_by_css_selector("li span a").click()
        self.node_url=self.driver.current_url


    def test_node_rename_log(self):
        """
        test to make sure that project log works correctly on renaming the node

        """

        #rename the project
        node_new_name=str(uuid.uuid1())[:6]
        util.project_rename(self.driver, node_new_name)

         #get log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " changed the title from "
                                               + config.node_title + " to " + node_new_name)


        #check the user_url and node_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1]+"/", self.node_url)


    def test_node_wiki_changes_log(self):
        """
        test to make sure that project log works correctly on a node wiki change

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


        #check the user_url and node_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1], wiki_url)


    def test_node_create_fork_log(self):
        """
        test to make sure that a project log works correctly on forking a correct node

        """
        #fork the project
        self.get_element(
            'a[data-original-title="Number of times this node has been forked (copied)"]').click()

        #get log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log text
        self.assertEqual(message_log.log_text
            , self.user_data["fullname"] + " created fork from node" + config.node_title)

        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1]+"/", self.node_url)


    def test_node_add_contributor_log(self):
        """
        test to make sure that project log works correctly on adding contributor to a node

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
        util.create_project(self.driver)
        util.create_node(self.driver)
        self.driver.find_element_by_css_selector("li span a").click()
        new_node_url=self.driver.current_url

        #add contributor
        self.add_contributor(self.user_data)

        #get log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, second_user_data["fullname"] + " added " + self.user_data['fullname']
                                               + " as contributor on node " + config.node_title)

        #check the second user_url, first user_url and node_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1], user_url)
        self.assertEqual(message_log.log_url[2]+"/", new_node_url)


    def test_node_delete_contributor_log(self):
        """
        test to make sure that project log works correctly on removing contributor from a node

        """

        # log out
        self.log_out()

        # create the second user
        second_user = self.create_user()

        # log back in as the first user
        self.log_in()

        # create the component
        title = 'Test Component'
        component_url = self.add_component('hypothesis', title)

        self.driver.get(component_url)

        # add contributor
        self.add_contributor(second_user)

        time.sleep(3)

        # remove contributor
        self.remove_contributor(second_user)

        # get log
        self.goto('dashboard')
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(
            message_log.log_text,
            '{} removed {} as a contributor from node {}'.format(
                self.user_data['fullname'],
                second_user['fullname'],
                title,
            )
        )

        #check the second user_url, first user_url and node_url
        # self.assertEqual(message_log.log_url[0], self.get_user_url())
        # self.assertEqual(message_log.log_url[1], user_url)
        self.assertEqual(
            message_log.log_url[2],
            component_url.strip('/')
        )


    def test_node_file_upload_log(self):
        """
        test to make sure that project log works correctly on uploading files to a node

        """
         # Test file names
        self.images = self._generate_full_filepaths({
            'jpg': 'test.jpg',
            'png': 'test.png',
            'gif': 'test.gif',
        })

        #Add a file to a project
        f = self.images['jpg']
        util.goto_project(self.driver, config.node_title)
        self.driver.find_element_by_link_text("Files").click()
        self.driver.execute_script('''
            $('input[type="file"]').offset({left : 50});
        ''')
        field = self.driver.find_element_by_css_selector('input[type=file]')
        field.send_keys(f['path'])
        self.driver.find_element_by_css_selector(
            'div.fileupload-buttonbar button.start'
        ).click()


        #get the log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " added file " + f['filename']
                                               + " to node " + config.node_title)

        #check the user_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())

        #check the node_url
        # the node_url is currently not correct, osf code need to be fixed
        self.assertEqual(message_log.log_url[1]+'/', self.node_url)


    def test_node_file_modification_log(self):
        """
        test to make sure that project log works correctly on modifying files on a project

        """
        # Test file names
        self.text_files = self._generate_full_filepaths({
            'txt': 'txtfile.txt',
            'html': 'htmlfile.html',
        })

        self.versioned_files = self._generate_full_filepaths({
            0: 'versioned-0.txt',
            1: 'versioned-1.txt',
        })

        #Add a file to a project
        filename = 'versioned.txt'
        upload_dir = os.path.dirname(self.text_files['txt']['path'])
        f = os.path.join(upload_dir, filename)

        # rename and upload version 0.
        shutil.copy(self.versioned_files[0]['path'], f)
        util.goto_project(self.driver, config.node_title)
        self.driver.find_element_by_link_text("Files").click()
        self.driver.execute_script('''
            $('input[type="file"]').offset({left : 50});
        ''')
        field = self.driver.find_element_by_css_selector('input[type=file]')
        field.send_keys(f)
        self.driver.find_element_by_css_selector(
            'div.fileupload-buttonbar button.start'
        ).click()

        # rename and upload version 1
        shutil.copy(self.versioned_files[1]['path'], f)
        util.goto_project(self.driver, config.node_title)
        self.driver.find_element_by_link_text("Files").click()
        self.driver.execute_script('''
            $('input[type="file"]').offset({left : 50});
        ''')
        field = self.driver.find_element_by_css_selector('input[type=file]')
        field.send_keys(f)
        self.driver.find_element_by_css_selector(
            'div.fileupload-buttonbar button.start'
        ).click()

        # delete the temp file
        os.remove(f)

        #get the log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " updated file " + filename
                                               + " in node " + config.node_title)

        #check the user_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())

        #check the node_url
        # the node_url is currently not correct, osf code need to be fixed
        self.assertEqual(message_log.log_url[1]+'/', self.node_url)


    def test_node_delete_file_log(self):
        """
        test to make sure that project log works correctly on deleting files from a node

        """
        # Test file names
        self.images = self._generate_full_filepaths({
            'jpg': 'test.jpg',
            'png': 'test.png',
            'gif': 'test.gif',
        })

        #Add a file to a project
        f = self.images['jpg']
        util.goto_project(self.driver, config.node_title)
        self.driver.find_element_by_link_text("Files").click()
        self.driver.execute_script('''
            $('input[type="file"]').offset({left : 50});
        ''')
        field = self.driver.find_element_by_css_selector('input[type=file]')
        field.send_keys(f['path'])
        self.driver.find_element_by_css_selector(
            'div.fileupload-buttonbar button.start'
        ).click()

        #delete the added file
        util.goto_project(self.driver, config.node_title)
        self.driver.find_element_by_link_text("Files").click()
        self.driver.find_element_by_css_selector('td form button').click()

        #get the log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " removed file " + f['filename']
                                               + " from node " + config.node_title)

        #check the user_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())

        #check the node_url
        # the node_url is currently not correct, osf code need to be fixed
        self.assertEqual(message_log.log_url[1]+'/', self.node_url)
