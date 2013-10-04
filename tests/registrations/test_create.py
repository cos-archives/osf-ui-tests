from nose.tools import *

from pages.fixtures import (
    ProjectRegistrationTestCase,
    SubprojectRegistrationTestCase,
)



class Create(object):

    def test_meta(self):
        assert_equal(
            self.page.registration_meta,
            self.registration_meta,
        )

    def test_template(self):
        assert_equal(
            self.page.registration_template,
            self.registration_template,
        )

    def test_title(self):
        assert_equal(
            self.parent_values['title'],
            self.page.title,
        )

    def test_component_list(self):
        assert_equal(
            self.parent_values['component_names'],
            self.page.component_names,
        )

    def test_contributors(self):
        assert_equal(
            self.parent_values['contributors'],
            self.page.contributors,
        )

    def test_date_created(self):
        assert_equal(
            self.parent_values['date_created'],
            self.page.date_created,
        )

    def test_last_udpated(self):
        assert_equal(
            self.parent_values['last_updated'],
            self.page.last_updated,
        )

    def test_logs(self):
        assert_equal(
            self.parent_values['logs'],
            self.page.logs,
        )


class FromProject(Create, ProjectRegistrationTestCase):
    pass


class FromSubproject(Create, SubprojectRegistrationTestCase):
    pass