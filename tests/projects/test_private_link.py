from nose.tools import *

from tests.fixtures import ComplexProjectFixture
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import ProjectPage
from pages.helpers import create_user


class PrivateLink(ComplexProjectFixture):

    @classmethod
    def setUpClass(cls):
        super(PrivateLink, cls).setUpClass()
        cls.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Settings'
        ).click()
        cls.page.driver.find_element_by_css_selector(
            'div#linkScope.col-md-6 button#generate-private-link.private-link'
        ).click()
        cls.page.driver.find_element_by_css_selector(
            'div.container div#private-link.modal.fade.in div.modal-content a.btn.btn-success'
        ).click()
        WebDriverWait(cls.page.driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'p#contributors span.contributor a')
            )
        )
        cls.page = ProjectPage(driver=cls.page.driver)
        cls.link = cls.page.driver.find_element_by_css_selector(
            'div#linkScope.col-md-6 li.contributor-list-item.list-group-item a.link-name'
        ).text
        cls.private_link = 'localhost:5000' + str(cls.link)[32:]
        cls.page.log_out()
        cls.users.append(create_user())
        cls.log_in(cls.users[-1])
        cls.page.driver.get(cls.private_link)
        WebDriverWait(cls.page.driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'p#contributors span.contributor a')
            )
        )

    def test_dashboard(self):
        self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Dashboard'
        ).click()
        WebDriverWait(self.page.driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'p#contributors span.contributor a')
            )
        )
        assert_equal(1, len(self.page.driver.fine_elements_by_css_selector(
            "h1#nodeTitleEditable"
        )))