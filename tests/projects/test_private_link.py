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
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "h1#nodeTitleEditable"
        )))
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "DIV#containment.col-md-7 SECTION#Files DIV#myGrid.dash-page.hgrid DIV.grid-canvas DIV.slick-cell.l0.r0.cell-title SPAN.folder.folder-open"
        )))
        assert_true(len(self.page.driver.find_elements_by_css_selector(
            "DIV.col-md-5 DIV#logScope DL.dl-horizontal.activity-log dt"
        )) > 1)
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "DIV.col-md-4 DIV.btn-toolbar.node-control.pull-right DIV.btn-group BUTTON.btn.btn-default.disabled"
        )))
        assert_equal(2, len(self.page.driver.find_elements_by_css_selector(
            "DIV.col-md-4 DIV.btn-toolbar.node-control.pull-right DIV.btn-group A.btn.btn-default.disabled"
        )))
        assert_equal("Private Component", self.page.driver.find_elements_by_css_selector(
            "DIV#containment.col-md-7 SECTION#Nodes UL.list-group LI.project.list-group-item.list-group-item-node.unavailable"
        )[0].find_element_by_css_selector("h4").text)

    def test_registration(self):
        self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Registrations'
        ).click()
        WebDriverWait(self.page.driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'p#contributors span.contributor a')
            )
        )
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "h1#nodeTitleEditable"
        )))

    def test_fork(self):
        self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Forks'
        ).click()
        WebDriverWait(self.page.driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'p#contributors span.contributor a')
            )
        )
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "h1#nodeTitleEditable"
        )))

    def test_statistics(self):
        self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Statistics'
        ).click()
        WebDriverWait(self.page.driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'p#contributors span.contributor a')
            )
        )
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "h1#nodeTitleEditable"
        )))

    def test_wiki(self):
        self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Wiki'
        ).click()
        WebDriverWait(self.page.driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'p#contributors span.contributor a')
            )
        )
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "h1#nodeTitleEditable"
        )))
        assert_equal(2, len(self.page.driver.find_elements_by_css_selector(
            "DIV.col-md-3 NAV.subnav.navbar.navbar-default UL.nav.navbar-nav li a.disabled"
        )))

    def test_file(self):
        self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Files'
        ).click()
        WebDriverWait(self.page.driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'p#contributors span.contributor a')
            )
        )
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "h1#nodeTitleEditable"
        )))
        assert_equal("test.jpg", self.page.driver.find_element_by_css_selector(
            "DIV#myGrid.dropzone.files-page div.grid-canvas div.ui-widget-content:nth-child(4) > div:nth-child(1) a"
        ).text)
        assert_equal(1, len(self.page.driver.find_elements_by_css_selector(
            "DIV#myGrid.dropzone.files-page div.grid-canvas div.ui-widget-content:nth-child(4) > div:nth-child(4) button"
        )))

    def test_no_settings(self):
        settingtab = self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_elements_by_link_text(
            'Settings'
        )
        assert_equal(0, len(settingtab))


class PrivateLinkRemove(ComplexProjectFixture):

    @classmethod
    def setUpClass(cls):
        super(PrivateLinkRemove, cls).setUpClass()
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
        cls.page.driver.find_element_by_css_selector(
            'div#linkScope.col-md-6 li.contributor-list-item.list-group-item a.remove-private-link'
        ).click()
        cls.page.driver.find_element_by_css_selector(
            'div.bootbox.modal.fade.in div.modal-content button.btn.btn-primary'
        ).click()
        cls.page = ProjectPage(driver=cls.page.driver)
        cls.page.log_out()
        cls.users.append(create_user())
        cls.log_in(cls.users[-1])

    def test_no_acess(self):
        self.page.driver.get(self.private_link)
        assert_in("Forbidden", self.page.driver.find_element_by_css_selector(
            "DIV.container DIV.col-md-12 h2#error"
        ).text)
