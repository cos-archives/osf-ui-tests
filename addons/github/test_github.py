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


class GithubaddonForkTests(GithubaddonFixture):
    @classmethod
    def setUpClass(cls):
        super(GithubaddonForkTests, cls).setUpClass()
        old_id = cls.page.id
        url = cls.page.driver.current_url
        cls.users.append(create_user())
        cls.page.add_contributor(cls.users[-1])
        cls.page.log_out()
        cls.log_in(cls.users[-1])

        cls.page = cls.page.node(old_id)
        cls.page.driver.get(url)
        cls.page = cls.page.fork()

    def test_alert_present(self):
        text = self.page.driver.find_element_by_css_selector(
            "DIV.container DIV#alert-container "
            "DIV.alert.alert-block.alert-warning.fade.in p"
        ).text
        assert_in("GitHub authorization not copied to forked project.", text)

    def test_widget_not_present(self):
        self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'Dashboard'
        ).click()

        assert_equal(
            len(self.page.driver.find_elements_by_css_selector(
                "DIV.container DIV#containment.col-md-7 "
                "DIV.addon-widget-container DIV.addon-widget div "
                "DIV.addon-config-error")
            ),
            1
        )

    def test_githubpage_not_present(self):
        self.page.driver.find_element_by_css_selector(
            'HEADER#overview.subhead UL.nav.navbar-nav'
        ).find_element_by_link_text(
            'GitHub'
        ).click()

        assert_equal(
            len(self.page.driver.find_elements_by_css_selector(
                "div.watermarked DIV.container div DIV.addon-config-error")
            ),
            1
        )


class GithubaddonRegistrationTests(GithubaddonFixture):

    registration_template = 'Open-Ended Registration'
    registration_meta = ('sample narrative', )

    @classmethod
    def setUpClass(cls):
        super(GithubaddonRegistrationTests, cls).setUpClass()

        cls.parent_values = {
            'title': cls.page.title,
            'component_names': cls.page.component_names,
            'contributors': cls.page.contributors,
            'date_created': cls.page.date_created,
            'last_updated': cls.page.last_updated,
            'logs': cls.page.logs,
            'url': cls.page.driver.current_url,

        }

        cls.page = cls.page.add_registration(
            registration_type=cls.registration_template,
            meta=cls.registration_meta,
        )

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

    def test_file_cannot_change(self):
        assert_equal(
            len(self.page.driver.find_elements_by_css_selector(
                "div.container div.addon-content div#grid div#gitGrid "
                "div.slick-viewport div.grid-canvas "
                "div.ui-widget-content.slick-row.odd div.slick-cell.l2.r2 "
                "div button.btn.btn-danger.btn-mini"
            )),
            0
        )


class GithubaddonSetPrivateTests(GithubaddonFixture):
    @classmethod
    def setUpClass(cls):
        super(GithubaddonSetPrivateTests, cls).setUpClass()
        cls.page.public = True

    def test_alert_present(self):
        text = self.page.driver.find_element_by_css_selector(
            "DIV.container DIV#alert-container "
            "DIV.alert.alert-block.alert-warning.fade.in p"
        ).text
        assert_in(
            "Warnings: This OSF project is public, but the GitHub repo osftest / addontesting is private.",
            text
        )