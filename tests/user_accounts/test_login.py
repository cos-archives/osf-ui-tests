from nose.tools import *

from tests.user_accounts.fixtures import LoginUserFixture


class UserLoginTest(LoginUserFixture):

    def test_login(self):
        self.log_in()
        assert_true(self.page.logged_in)
        self.page.close()

    def test_no_email_and_no_password(self):
        self.log_in_check("", "")
        assert_equal(len(self.page.alerts), 2)
        assert_in('Email address is required', self.page.alerts[0])
        assert_in('Password is required', self.page.alerts[1])
        self.page.close()

    def test_no_email(self):
        self.log_in_check('', 'badpassword')
        assert_equal(len(self.page.alerts), 1)
        assert_in('Email address is required', self.page.alerts[0])
        self.page.close()

    def test_no_password(self):
        self.log_in_check(self.users[-1].email, '')
        assert_equal(len(self.page.alerts), 1)
        assert_in('Password is required', self.page.alerts[0])
        self.page.close()

    def test_not_registered_email(self):
        self.log_in_check('bad@email.addr', self.users[-1].password)
        assert_equal(len(self.page.alerts), 1)
        assert_in(
            'Log-in failed. Please try again or reset your password',
            self.page.alerts[0]
        )

    def test_incorrect_password(self):
        self.log_in_check(self.users[-1].email, 'wrongpass')
        assert_equal(len(self.page.alerts), 1)
        assert_in(
            'Log-in failed. Please try again or reset your password',
            self.page.alerts[0]
        )
        self.page.close()

    def test_log_out(self):
        self.log_in()
        self.page.log_out()
        assert_equal(
            len(self.page.get_alert_boxes('You have successfully logged out.')),
            1
        )
        self.page.close()
