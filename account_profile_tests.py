"""
Selenium test suite for account profile manipulation and access
Author: Harry Rybacki
Date: 29May13
"""
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AccountProfileTest(unittest.TestCase):

    # initialize a Firefox webdriver
    def setUp(self):
        # setup browser and test user data
        self.driver = webdriver.Firefox()
        self.user_email = 'test@test.com'
        self.user_password = 'testtest'
        self.user_name = 'Testy McTester'

        # ensure driver allows page source to load before getting fields
        self.driver.implicitly_wait(30)

        # load OSF homepage
        self.driver.get('http://localhost:5000')
        # load login page
        self.driver.find_element_by_xpath('//a[@href="/account"]').click()

        # grab the username and password fields
        username_field = self.driver.find_elements_by_xpath('//form[@name="signin"]//input[@id="username"]')
        password_field = self.driver.find_elements_by_xpath('//form[@name="signin"]//input[@id="password"]')

        # enter the username / password
        username_field[0].send_keys(self.user_email)
        password_field[0].send_keys(self.user_password)

        # locate and click login button
        submit_buttons = self.driver.find_elements_by_xpath('//button[@type="submit"]')
        submit_button = [b for b in submit_buttons if b.text.lower() == 'sign in'][0]
        submit_button.click()

        # grab the profile button and load the page
        profile_button = self.driver.find_element_by_link_text('My Public Profile')
        profile_button.click()

    # close the Firefox webdriver
    def tearDown(self):
        self.driver.close()

    def test_access_profile(self):
        """
        tests user ability to access page and verifies name on profile page
        matches expected test data
        """
        profile_name = self.driver.find_element_by_id('profile-dfullname').text
        self.assertTrue(self.user_name in profile_name)

    def test_change_name(self):
        """
        tests user ability to change username and asserts the change is made
        before changing it back to the original
        """
        # select and click the username edit field
        edit_profile_name_button = self.driver.find_element_by_id(
            'profile-fullname')
        edit_profile_name_button.click()

        # select the name field on the new popup
        edit_profile_name_field = self.driver.find_element_by_xpath(
            '//div[@class="popover-content"]//input[@class="span2"]')

        # delete the current name
        for i in range(len(self.user_name)):
            edit_profile_name_field.send_keys(Keys.BACK_SPACE)

        # enter the reverse user name
        edit_profile_name_field.send_keys(self.user_name[::-1])

        # find and click submit new name
        edit_profile_name_submit_button = self.driver.find_element_by_xpath(
            '//div[@class="popover-content"]//button[@class="btn btn-primary"]'
        )
        edit_profile_name_submit_button.click()

        # refresh page and assert change was made
        self.driver.refresh()
        profile_name = self.driver.find_element_by_id('profile-dfullname').text
        self.assertTrue(self.user_name[::-1] in profile_name)

        # return the username back to its original -- same as above
        edit_profile_name_button = self.driver.find_element_by_id(
            'profile-fullname')
        edit_profile_name_button.click()
        edit_profile_name_field = self.driver.find_element_by_xpath(
            '//div[@class="popover-content"]//input[@class="span2"]')
        for i in range(len(self.user_name)):
            edit_profile_name_field.send_keys(Keys.BACK_SPACE)
        edit_profile_name_field.send_keys(self.user_name)
        edit_profile_name_submit_button = self.driver.find_element_by_xpath(
            '//div[@class="popover-content"]//button[@class="btn btn-primary"]'
        )
        edit_profile_name_submit_button.click()

        # refresh page and assert username is back to the original
        self.driver.refresh()
        profile_name = self.driver.find_element_by_id('profile-dfullname').text
        self.assertTrue(self.user_name in profile_name)

    @unittest.skip("not an implemented feature in OSF codebase")
    def test_change_location(self):
        pass

    def test_click_public_shortlink(self):
        """
        tests user ability to click profile short link and be direted to their
        profile.

        Note: We are checking against the name because Selenium
        doesn't currently have the ability to monitor redirects or check
        HTTP status codes.
        """
        # find and click user's profile shortlink
        public_profile_shortlink = self.driver.find_element_by_xpath(
            '//div[@class="span4"]//a')
        public_profile_shortlink.click
        # assert name still matches username
        profile_name = self.driver.find_element_by_id('profile-dfullname'
        ).text
        self.assertTrue(self.user_name in profile_name)

    @unittest.skip("not implemented")
    def test_check_public_project_updates(self):
        pass

if __name__ == '__main__':
    unittest.main()



