import unittest

from pages import helpers, LoginPage


class ApiContributorTestCase(unittest.TestCase):
    def setUp(self):
        # create a user
        self.user = helpers.create_user()

        # log them in
        self.browser = LoginPage().log_in(self.user)

        # create a new API key
        self.api_key = self.browser.settings.add_api_key()

    def tearDown(self):
        # close the browser
        self.browser.close()


class ApiNonContributorTestCase(unittest.TestCase):
    def setUp(self):
        # get the API key for an unrelated user
        page = LoginPage().log_in(helpers.create_user())
        self.api_key = page.settings.add_api_key()
        page.close()

        # create a user to use
        self.user = helpers.create_user()
        self.browser = LoginPage().log_in(self.user)

    def tearDown(self):
        # close the browser
        self.browser.close()


class ApiAnonymousTestCase(unittest.TestCase):
    def setUp(self):
        # create a user to use
        self.user = helpers.create_user()
        self.browser = LoginPage().log_in(self.user)

    def tearDown(self):
        # close the browser
        self.browser.close()