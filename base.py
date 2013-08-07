"""
Base classes for smoke tests. Test classes can subclass various
classes defined here instead of repetitively defining setUp and 
tearDown methods. Note: these classes do NOT inherit from 
unittest.TestCase. If subclasses need to be detected by unittest / 
nose, they must multiply inherit from TestCase. This is done to 
permit abstract test classes that will not be detected by unittest /
nose.
"""

# Imports
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

# Project imports
import config
import util


class SmokeTest(object):
    """Base class for smoke tests. Creates a WebDriver
    on setUp and quits on tearDown.

    """
    # Allow multiprocessing for individual tests
    _multiprocess_can_split_ = True

    def setUp(self):
        
        # Launch Selenium using options specified as class
        # variables, which can include driver_name and
        # desired_capabilities
        if hasattr(self, 'driver_opts'):
            self.driver = util.launch_driver(**self.driver_opts)
        else:
            self.driver = util.launch_driver()

        self.site_root = config.osf_home.strip('/')
        
    def tearDown(self):
        
        # Quit Selenium
        # Note: Use WebDriver.quit() instead of WebDriver.close();
        # otherwise, SauceLabs tests will never finish
        self.driver.quit()


class UserSmokeTest(SmokeTest):
    """Class for smoke tests that require user login.
    Creates a user and logs in on setUp and logs out on
    tearDown.

    """
    def setUp(self):
        
        # Call parent setUpClass
        super(UserSmokeTest, self).setUp()

        # Create user account and login
        self.user_data = util.create_user(self.driver)
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )

    def tearDown(self):
        
        # Log out
        util.logout(self.driver)

        # Call parent tearDown
        super(UserSmokeTest, self).tearDown()

        
class ProjectSmokeTest(UserSmokeTest):
    """Class for smoke tests that require project
    creation. Creates a project on setUp and deletes it
    on tearDown.

    """
    def setUp(self):
        
        # Call parent setUp
        super(ProjectSmokeTest, self).setUp()

        # Create test project
        self.project_url = util.create_project(self.driver)
    
        # Browse to project page
        util.goto_project(self.driver)
    
    def tearDown(self):
        
        # Delete test project
        util.delete_project(self.driver)

        # Call parent tearDown
        super(ProjectSmokeTest, self).tearDown()

    def goto(self, page, *args):
        """Go to a project's page

        :param page: The name of the destination page. Acceptable include
                     "files", "settings", and "registrations"
        :returns: True on success, KeyError page
        """
        build_path = {
            'dashboard': lambda: self.project_url,
            'files': lambda: '/'.join([self.project_url[:-1], 'files']),
            'file': lambda: '/'.join([self.project_url[:-1], 'files', args[0]]),
            'user-dashboard': lambda: '/'.join([self.site_root, 'dashboard'])
        }

        # This will throw a KeyError if the page type is not in the above dict.
        self.driver.get(
            url=build_path[page]()
        )

    def get_element(self, css):
        return wait(
            driver=self.driver,
            timeout=10
        ).until(
            method=ec.visibility_of_element_located(
                (By.CSS_SELECTOR, css)
            )
        )

    # User methods

    def create_user(self):
        return util.create_user(self.driver)

    def log_in(self, user=None):
        if not user:
            user = self.user_data
        return util.login(
            self.driver,
            user['username'],
            user['password']

        )

    def log_out(self):
        return util.logout(self.driver)

    # Node methods

    def add_contributor(self, user):
        # click the "add" link
        self.get_element('#contributors a[href="#addContributors"]').click()

        # enter the user's email address
        self.get_element('div#addContributors input[type=text]').send_keys(
            user['username']
        )

        # click the search button
        self.get_element('#addContributors button').click()

        # click the radio button for the first result
        self.get_element('#addContributors input[type=radio]').click()

        # click the "Add" button
        self.get_element('#addContributors button.btn.primary').click()

    def remove_contributor(self, user):

        self.driver.execute_script(
            """me = $('#contributors a:contains("{fullname}")')
                .append('<i class="icon-remove"><i>');
            removeUser(
                me.attr("data-userid"),
                me.attr("data-fullname"),
                me
            );""".format(fullname=user['fullname'])
        )

        self.driver.switch_to_alert().accept()