"""

"""

import unittest
import time

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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

    def _test_fork_list(self, page):
        """ Given a project, register it and verify that the new registration is
         in the project's registration list
        """
        _url = page.driver.current_url

        page = page.fork()

        page.driver.get(_url)

        try:
            return page.forks
        finally:
            page.close()

    def test_project_fork_listed(self):
        """After forking a project, the fork should be listed in the original
        project's Forks pane."""
        forks = self._test_fork_list(page=self._project())
        self.assertEqual(len(forks), 1)

    def test_subproject_fork_listed(self):
        """After forking a project, the fork should be listed in the original
        project's Forks pane."""
        forks = self._test_fork_list(page=self._subproject())
        self.assertEqual(len(forks), 1)

    def test_project_fork_list_title(self):
        """After forking a project, the fork should show the correct title in
        the project's Forks pane.
        """
        page = self._project()
        title = page.title

        self.assertEqual(
            self._test_fork_list(
                page=page
            )[0].title,
            'Fork of {}'.format(title),
        )

    def test_subproject_fork_list_title(self):
        """Subproject variant of ``self.test_project_fork_list_title``"""
        page = self._subproject()
        title = page.title

        self.assertEqual(
            self._test_fork_list(
                page=page
            )[0].title,
            'Fork of {}'.format(title),
        )

    def _test_fork_title(self, page):
        """Verify that a fork's title matches that of the original project -
        with a "Fork of " prefix.
        """
        original_title = page.title
        page = page.fork()
        self.assertEqual(
            page.title,
            'Fork of ' + original_title,
        )

        page.close()

    def test_project_fork_title(self):
        """Project variant of ``self.test_project_fork_list_title``"""
        self._test_fork_title(self._project())

    def test_subproject_fork_title(self):
        """Subproject variant of ``self.test_project_fork_list_title``"""
        self._test_fork_title(self._subproject())

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

    def test_project_fork_components_empty(self):
        """ Verify that a fork's (empty) component list matches the
        original project"""
        self._test_fork_matches(
            page=self._project(),
            attribute='component_names'
        )

    def test_subproject_fork_components_empty(self):
        """Subproject variant of ``self.test_project_fork_components_empty``"""
        self._test_fork_matches(
            page=self._subproject(),
            attribute='component_names'
        )

    def test_project_fork_components(self):
        """Verify that a fork's (non-empty) component list matches the original
        project"""
        page = self._project()

        # add component
        page = page.add_component(
            title='Test Component',
            component_type='Other',
        )

        page = page.parent_project()

        # add a subproject
        page = page.add_component(
            title='Test Subproject',
            component_type='Project',
        )

        page = page.parent_project()

        self._test_fork_matches(
            page=page,
            attribute='component_names'
        )

    def test_subproject_fork_components(self):
        """Subproject variant of ``self.test_project_fork_components``"""
        page = self._subproject()

        # add component
        page = page.add_component(
            title='Test Component',
            component_type='Other',
        )

        page = page.parent_project()

        self._test_fork_matches(
            page=page,
            attribute='component_names'
        )

    @unittest.skip('test not implemented')
    def test_project_fork_contributors(self):
        """Verify that a fork's contributor list matches the original project"""
        pass


    @unittest.skip('test not implemented')
    def test_subproject_fork_contributors(self):
        """Subproject variant of ``self._test_project_fork_contributors``"""
        pass

    def test_project_fork_created_date(self):
        """Verify that a fork's creation date matches the original project"""
        self._test_fork_matches(
            page=self._project(),
            attribute='date_created'
        )

    def test_subproject_fork_created_date(self):
        """Subproject variant of ``self._test_project_fork_created_date``"""
        self._test_fork_matches(
            page=self._subproject(),
            attribute='date_created'
        )

    def test_project_fork_wiki_home(self):
        """ Verify that a fork's wiki homepage content matches the original
        project """
        page = self._project()

        page.set_wiki_content('Test wiki content!')

        self._test_fork_matches(
            page=page,
            attribute='wiki_home_content'
        )

    def test_subproject_fork_wiki_home(self):
        """Subproject variant of ``self.test_project_fork_wiki_home``"""
        page = self._subproject()

        page.set_wiki_content('Test wiki content!')

        self._test_fork_matches(
            page=page,
            attribute='wiki_home_content'
        )

    def _test_fork_logged(self, page):
        """ Given a project, register it and verify that the action appears in
        the original project's logs.
        """
        user = page.contributors[0].full_name

        _url = page.driver.current_url
        title = page.title

        page = page.fork()

        self.assertEqual(
            page.logs[0].text,
            u'{user} created fork from project {title}'.format(
                user=user,
                title=title
            )
        )

        page.close()

    def test_project_fork_logged(self):
        """ Project variant of ``self._test_fork_logged`` """
        self._test_fork_logged(self._project())

    def test_subproject_fork_logged(self):
        """ Subproject variant of ``self._test_fork_logged`` """
        # TODO: This fails right now because a subproject is referred to as a
        # "node" in the log.
        self._test_fork_logged(self._subproject())



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
        time.sleep(2)
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

# Run tests
if __name__ == '__main__':
    unittest.main()
