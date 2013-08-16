"""
Tests for project logs.
"""

import time


# Project imports
import base
import util
import config
import uuid


class ProjectLogTests(base.ProjectSmokeTest):

    def test_create_project_log(self):
        """
        test to make sure that creating the project log works correctly

        """
        #get log
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log text
        self.assertEqual(
            message_log.log_text,
            u"{} created project".format(self.user_data["fullname"])
        )

        #check the user_url and project_url
        self.assertEqual(
            message_log.log_url[0],
            self.get_user_url()
        )
        self.assertEqual(
            message_log.log_url[1],
            self.project_url.strip('/')
        )

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
        self.assertEqual(
            message_log.log_text,
            u"{} created node {}".format(
                self.user_data["fullname"],
                config.node_title,
            )
        )

        #check the user_url
        self.assertEqual(
            message_log.log_url[0],
            self.get_user_url()
        )

        #get the node url
        self.driver.find_element_by_css_selector("li span a").click()
        node_url = self.driver.current_url

        # check the node url
        # this part currently failed because something need to be fixed on the
        # webpage
        self.assertEqual(
            message_log.log_url[1],
            node_url.strip('/')
        )

    def test_project_rename_log(self):
        """
        test to make sure that rename the project log works correctly

        """
        #get user_url
        user_url = self.get_user_url()

        #rename the project
        project_new_name = str(uuid.uuid1())[:6]
        util.project_rename(self.driver, project_new_name)

         #get log
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(
            message_log.log_text,
            u"{} changed the title from {} to {}".format(
                self.user_data["fullname"],
                config.project_title,
                project_new_name,
                )
        )

        #check the user_url and project_url
        self.assertEqual(
            message_log.log_url[0],
            user_url,
        )
        self.assertEqual(
            message_log.log_url[1],
            self.project_url.strip('/'),
        )

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

    def test_create_fork_log(self):
        """
        test to make sure that fork a project log works correctly

        """
        #fork the project
        self.get_element(
            'a[data-original-title="Number of times this node has been forked (copied)"]').click()

        #get log
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log text
        self.assertEqual(message_log.log_text
            , self.user_data["fullname"] + " created fork from project" + config.project_title)

        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1]+"/", self.project_url)


    def test_add_contributor_log(self):
        """
        test to make sure that add contributor log works correctly

        """
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

        #get log
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(
            message_log.log_text,
            u'{} added {} as contributor on node {}'.format(
                second_user_data['fullname'],
                self.user_data['fullname'],
                config.project_title,
            )
        )

        #check the user_url and project_url
        self.assertEqual(
            message_log.log_url[0],
            self.get_user_url()
        )
        self.assertEqual(
            message_log.log_url[1],
            user_url
        )
        self.assertEqual(
            message_log.log_url[2],
            project_url.strip('/')
        )

    def test_delete_contributor_log(self):
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

        time.sleep(3)

        #remove contributor
        self.remove_contributor(self.user_data)

        time.sleep(3)

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
        self.assertEqual(message_log.log_url[2]+"/", project_url)

    def test_file_upload_log(self):
        """
        test to make sure that project log works correctly on uploading files to a project

        """
         # Test file names
        self.images = self._generate_full_filepaths({
            'jpg': 'test.jpg',
            'png': 'test.png',
            'gif': 'test.gif',
        })

        #Add a file to a project
        f = self.images['jpg']
        self.add_file(f['path'])

        #get the log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " added file " + f['filename']
                                               + " to project " + config.project_title)

        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1]+'/', self.project_url)

    def test_file_modification_log(self):
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
        f = self.add_versioned_file()

        #get the log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " updated file " + f
                                               + " in project " + config.project_title)

        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1]+'/', self.project_url)

    def test_delete_file_log(self):
        """
        test to make sure that project log works correctly on deleting files from a project

        """
        # Test file names
        self.images = self._generate_full_filepaths({
            'jpg': 'test.jpg',
            'png': 'test.png',
            'gif': 'test.gif',
        })

        #add a file
        f = self.images['jpg']
        self.add_file(f['path'])

        #delete the added file
        self.goto('files')
        self.driver.find_element_by_css_selector('td form button').click()

        #get the log
        util.goto_project(self.driver)
        message_log = self.get_log()

        #assert the time
        self._assert_time(message_log.log_time)

        #assert the log
        self.assertEqual(message_log.log_text, self.user_data["fullname"] + " removed file " + f['filename']
                                               + " from project " + config.project_title)

        #check the user_url and project_url
        self.assertEqual(message_log.log_url[0], self.get_user_url())
        self.assertEqual(message_log.log_url[1]+'/', self.project_url)
