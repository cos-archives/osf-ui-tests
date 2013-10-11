import config

from nose.tools import *

from pages.auth import UserProfilePage
from tests.fixtures import UserFixture


class ProfileTest(UserFixture):
    def setUp(self):
        super(ProfileTest, self).setUp()
        profile_url = '/'.join((config.osf_home, 'profile/'))

        self.page.driver.get(profile_url)
        self.page = UserProfilePage(driver=self.page.driver)

    def test_header(self):
        assert_equal(self.page.full_name, self.users[0].full_name)

    def test_public_shortlink(self):
        self.page.driver.get(self.page.profile_shortlink)
        assert_equal(self.page.full_name, self.users[0].full_name)


class ChangeNameTest(UserFixture):
    def setUp(self):
        super(ChangeNameTest, self).setUp()
        profile_url = '/'.join((config.osf_home, 'profile/'))

        self.page.driver.get(profile_url)
        self.page = UserProfilePage(driver=self.page.driver)

        self.page.full_name = 'Changed Name'

        self.page.driver.get(profile_url)

    def test_change_name(self):
        assert_equal('Changed Name', self.page.full_name)