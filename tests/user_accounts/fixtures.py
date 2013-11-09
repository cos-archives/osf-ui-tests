import time
import unittest

import requests

import config
from pages import FILES, helpers, LoginPage
from pages.generic import OsfPage
from tests.fixtures import UserFixture, OsfBaseFixture


class LoginUserFixture(OsfBaseFixture):
    @classmethod
    def setUp(cls):
        super(LoginUserFixture, cls).setUpClass()
        cls.create_user()



