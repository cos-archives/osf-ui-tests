from nose.tools import *

from tests.fixtures import ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentOfProjectFixture
from tests.components.fixtures import ComponentOfSubprojectFixture
import uuid
import datetime as dt


class WikiFixture(object):
    @classmethod
    def setUpClass(cls):
        super(WikiFixture, cls).setUpClass()
        cls.project_url = cls.page.driver.current_url
        cls.wiki_version = cls.page.get_wiki_version()
        cls.new_content = str(uuid.uuid1())[:20]
        cls.page.set_wiki_content(cls.new_content)
        cls.wiki_version += 1

    def test_logged(self):
        assert_equal(
            u'{} updated wiki page home to version {}'.format(
                self.users[0].full_name,
                self.wiki_version,
            ),
            self.page.logs[0].text,
        )

    def test_project_links(self):
        assert_equal(
            self.page.driver.current_url + "wiki/home",
            self.page.logs[0].links[1].url
        )

    def test_user_links(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )


class ProjectWiki(WikiFixture, ProjectFixture):
    pass


class SubprojectWiki(WikiFixture, SubprojectFixture):
    pass


class ComponentOfProjectWikiTest(
    WikiFixture,
    ComponentOfProjectFixture
):
    pass


class ComponentOfSubprojectWikiTest(
    WikiFixture,
    ComponentOfSubprojectFixture
):
    pass


class NewWikiPageFixture(object):
    @classmethod
    def setUpClass(cls):
        super(NewWikiPageFixture, cls).setUpClass()
        cls.project_url = cls.page.driver.current_url
        cls.new_wiki_name= str(uuid.uuid1())[:5]
        cls.new_content = str(uuid.uuid1())[:20]
        cls.link = cls.page.new_wiki_page(cls.new_wiki_name, cls.new_content)

    def test_logged(self):
        assert_equal(
            u'{} updated wiki page {} to version 1'.format(
                self.users[0].full_name,
                self.new_wiki_name,
            ),
            self.page.logs[0].text,
        )

    def test_project_log_links(self):
        assert_equal(
            self.page.driver.current_url + "wiki/"+self.new_wiki_name,
            self.page.logs[0].links[1].url
        )

    def test_wiki_page_link(self):
        assert_equal(
            self.page.driver.current_url + "wiki/"+self.new_wiki_name+'/',
            self.link
        )

    def test_user_links(self):
        assert_equal(
            self.user_profile_url,
            self.page.logs[0].links[0].url
        )

    def test_date_created(self):
        assert_almost_equal(
            self.page.logs[0].date,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )


class ProjectNewWiki(NewWikiPageFixture, ProjectFixture):
    pass


class SubprojectNewWiki(NewWikiPageFixture, SubprojectFixture):
    pass


class ComponentOfProjectNewWikiTest(
    NewWikiPageFixture,
    ComponentOfProjectFixture
):
    pass


class ComponentOfSubprojectNewWikiTest(
    NewWikiPageFixture,
    ComponentOfSubprojectFixture
):
    pass