from addons.github.fixture import GithubaddonFixture
from pages.helpers import create_user
from pages import FILES
from nose.tools import *
import datetime as dt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WidgetTests(GithubaddonFixture):

    def test_widget(self):
        assert_in(
            "branch",
            self.page.driver.find_element_by_css_selector('div.updated').text
        )


class GithubPageTests(GithubaddonFixture):
    @classmethod
    def setUpClass(cls):
        super(GithubPageTests, cls).setUpClass()
        cls.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'GitHub'
        ).click()
        WebDriverWait(cls.page.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 "div.container div.addon-content div#grid div#gitGrid "
                 "div.slick-viewport div.grid-canvas ")
            )
        )

    def test_download_present(self):
        assert_equal(
            len(self.page.driver.find_elements_by_css_selector(
                "div.container div.addon-content div#grid div#gitGrid "
                "div.slick-viewport div.grid-canvas "
                "div.ui-widget-content.slick-row.odd div.slick-cell.l2.r2 "
                "div button.btn.btn-danger.btn-mini"
            )),
            1
        )

    def test_branch_present(self):
        assert_equal(
            len(self.page.driver.find_elements_by_css_selector(
                "div.container div.addon-content div.row div.col-md-6 div form "
                "SELECT#gitBranchSelect"
            )),
            1
        )


class GithubaddonAddContributorTests(GithubaddonFixture):
    @classmethod
    def setUpClass(cls):
        super(GithubaddonAddContributorTests, cls).setUpClass()
        cls.users.append(create_user())
        cls.page.add_contributor(cls.users[-1])
        cls.old_id = cls.page.id

    def test_contributor_added(self):
        assert_equal(2, len(self.page.contributors))

    def test_contributor_present(self):
        assert_equal(self.users[-1].full_name, self.page.contributors[-1].full_name)

    def test_logged(self):
        assert_equal(
            u'{} added {} to {} {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.type,
                self.page.title,
            ),
            self.page.logs[0].text,
        )

    def test_project_links(self):
        assert_equal(
            self.page.driver.current_url,
            self.page.logs[0].links[2].url
        )

    def test_user_links(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url
        )
        assert_in(
            self.page.log_user_link(self.users[-1])[-6:],
            self.page.logs[0].links[1].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )


class GithubaddonRemoveContributorTests(GithubaddonFixture):
    @classmethod
    def setUpClass(cls):
        super(GithubaddonRemoveContributorTests, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())

        cls.page.add_multi_contributor(cls.users[1], cls.users[2])

        cls.page.remove_contributor(cls.users[1])
        cls.old_id = cls.page.id

    def test_contributor_removed(self):
        assert_equal(2, len(self.page.contributors))

    def test_logged(self):
        assert_equal(
            u'{} removed {} as a contributor from {} {}'.format(
                self.users[0].full_name,
                self.users[1].full_name,
                self.page.type,
                self.page.title,
            ),
            self.page.logs[0].text,
        )

    def test_project_links(self):
        assert_equal(
            self.page.driver.current_url,
            self.page.logs[0].links[2].url
        )

    def test_user_links(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url
        )
        assert_in(
            self.page.log_user_link(self.users[1]),
            self.page.logs[0].links[1].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )



 #registration

#public/private switch
