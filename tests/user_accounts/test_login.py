from nose.tools import *

from tests.fixtures import UserFixture, OsfBaseFixture
from tests.user_accounts.fixtures import LoginUserFixture



class UserLoginCorrect(LoginUserFixture):
    def test_login(self):
        self.log_in()
        assert_true(self.page.logged_in)


class UserLoginNoEmailNoPassword(LoginUserFixture):
    def test_login(self):
        self.log_in_check("", "")
        assert_equal(
            len(self.page.get_alert_boxes('Email address is required')),
            1
        )
