from nose.tools import *

from tests.fixtures import UserFixture, OsfBaseFixture
from tests.user_accounts.fixtures import LoginUserFixture
import util


class UserLoginCorrect(LoginUserFixture):
    def test_login(self):
        self.log_in()
        assert_true(self.page.logged_in)


class UserLoginNoEmailNoPassword(LoginUserFixture):
    def test_no_email_and_no_password(self):
        self.log_in_check("", "")
        assert_equal(
            len(self.page.get_alert_boxes('Email address is required')),
            1
        )
        assert_equal(
            len(self.page.get_alert_boxes('Password is required')),
            1
        )


class UserLoginNoEmail(LoginUserFixture):
    def test_no_email(self):
        self.log_in_check('', 'badpassword')
        assert_equal(
            len(self.page.get_alert_boxes('Email address is required')),
            1
        )


class UserLoginNoPassword(LoginUserFixture):
    def test_no_password(self):
        self.log_in_check(self.users[-1].email, '')
        assert_equal(
            len(self.page.get_alert_boxes('Email address is required')),
            1
        )


class UserLoginNotRegisteredEmail(LoginUserFixture):
    def test_not_registered_email(self):
        self.log_in_check('bad@email.addr', self.users[-1].password)
        assert_equal(
            len(self.page.get_alert_boxes('log-in failed')),
            1
        )


class UserLoginIncorrectPassword(LoginUserFixture):
    def test_incorrect_password(self):
        self.log_in_check(self.users[-1].email, 'wrongpass')
        assert_equal(
            len(self.page.get_alert_boxes('log-in failed')),
            1
        )

class UserLogoutTest(LoginUserFixture):
    def test_log_out(self):
        self.log_in()
        util.logout(self.page.driver)
        assert_equal(
            len(self.page.get_alert_boxes('You have successfully logged out.')),
            1
        )