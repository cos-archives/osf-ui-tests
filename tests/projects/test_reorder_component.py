from nose.tools import *

from pages.project import ProjectPage
from tests.fixtures import ProjectFixture
from selenium.webdriver import ActionChains


class ReorderComponentTest(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(ReorderComponentTest, cls).setUpClass()
        cls.project_url = cls.page.driver.current_url
        cls.page.add_component(
            title='first',
            component_type='hypothesis',
        )
        cls.page.driver.get(cls.project_url)
        cls.page.add_component(
            title='second',
            component_type='hypothesis',
        )
        cls.title = cls.page.title
        cls.page.driver.get(cls.project_url)

        # Second method: by element
        ac = ActionChains(cls.page.driver)
        a = cls.page.driver.find_element_by_css_selector('#Nodes li:first-child')
        b = cls.page.driver.find_element_by_css_selector('#Nodes li:last-child')
        ac.click_and_hold(a).perform()
        a_chain = ActionChains(cls.page.driver)
        a_chain.move_to_element(b).perform()
        a_chain.release(b).perform()

    def test_reorder_components(self):
        assert_equal(
            self.page.driver.find_element_by_css_selector(
                '#Nodes li:first-child h4 span a'
            ).text,
            self.title,
        )
