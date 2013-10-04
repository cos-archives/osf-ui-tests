from pages.fixtures import UserTestCase


class CreateUserTestCase(UserTestCase):

    def test_login(self):
        self.assertTrue(self.page.logged_in)