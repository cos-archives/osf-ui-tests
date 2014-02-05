from nose.tools import *
from pages.helpers import create_user
from tests.fixtures import ProjectFixture
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ReorderContributorTest(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(ReorderContributorTest, cls).setUpClass()
        cls.users.append(create_user())
        cls.page.add_contributor(cls.users[-1], children=True)
        cls.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Contributors'
        ).click()

        WebDriverWait(cls.page.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.col-md-7 div#contributors')
            )
        )
        # Second method: by element
        ac = ActionChains(cls.page.driver)
        a = cls.page.driver.find_elements_by_css_selector(
            'div.col-md-7 div#contributors li'
        )[0]
        b = cls.page.driver.find_elements_by_css_selector(
            'div.col-md-7 div#contributors li'
        )[1]
        ac.click_and_hold(a).perform()
        a_chain = ActionChains(cls.page.driver)
        a_chain.move_to_element(b).perform()
        a_chain.release(b).perform()

    def test_reorder_contributors(self):
        assert_equal(
            self.page.driver.find_elements_by_css_selector(
                'div.col-md-7 div#contributors li'
            )[0].find_elements_by_css_selector(
                'a'
            )[1].text,
            self.users[1].full_name,
        )

    def test_contributor_present(self):
        assert_equal(self.users[1].full_name, self.page.contributors[0].full_name)
        assert_equal(self.users[0].full_name, self.page.contributors[1].full_name)


class SortContributorTest(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(SortContributorTest, cls).setUpClass()
        cls.users.append(create_user())
        cls.page.add_contributor(cls.users[-1], children=True)
        cls.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Contributors'
        ).click()

        WebDriverWait(cls.page.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.col-md-7 div#contributors')
            )
        )

        cls.page.driver.find_element_by_css_selector(
            "button#sort"
        ).click()

        WebDriverWait(cls.page.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.modal-dialog div.modal-footer button.btn.btn-primary')
            )
        )

        cls.page.driver.find_element_by_css_selector(
            'div.modal-dialog div.modal-footer button.btn.btn-primary'
        ).click()

        WebDriverWait(cls.page.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'div.col-md-7 div#contributors')
            )
        )

    def test_sort_contributors(self):
        if self.users[1].full_name < self.users[0].full_name:
            assert_equal(
                self.page.driver.find_elements_by_css_selector(
                    'div.col-md-7 div#contributors li'
                )[0].find_elements_by_css_selector(
                    'a'
                )[1].text,
                self.users[1].full_name,
            )
        else:
            assert_equal(
                self.page.driver.find_elements_by_css_selector(
                    'div.col-md-7 div#contributors li'
                )[0].find_elements_by_css_selector(
                    'a'
                )[1].text,
                self.users[0].full_name,
            )

    def test_contributor_present(self):
        if self.users[1].full_name < self.users[0].full_name:
            assert_equal(self.users[1].full_name, self.page.contributors[0].full_name)
            assert_equal(self.users[0].full_name, self.page.contributors[1].full_name)
        else:
            assert_equal(self.users[0].full_name, self.page.contributors[0].full_name)
            assert_equal(self.users[1].full_name, self.page.contributors[1].full_name)
