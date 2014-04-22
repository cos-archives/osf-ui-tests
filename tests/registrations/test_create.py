from nose.tools import *

from tests.registrations.fixtures import (
    ProjectRegistrationFixture,
    SubprojectRegistrationFixture,
)


class Create(object):
    """ Create a registration.

    This class inherits from object because it is technically not a test suite.
    Below, it is subclassed twice - once for projects, and once for subprojects.

    Note that self.parent_values is defined in the fixture class. If there are
    additional attributes to be compared with their source project, those
    attributes must be added to the fixture as well.
    """

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

    def test_last_updated(self):
        assert_equal(
            self.parent_values['last_updated'],
            self.page.last_updated,
        )

    def test_logs(self):
        assert_equal(
            self.parent_values['logs'],
            self.page.logs,
        )

    def test_link_to_source_project(self):
        assert_equal(
            self.parent_values['url'],
            self.page.source_link,
        )

    def test_file_upload_disabled(self):
        assert_false(self.page.can_add_file)

    def test_file_deletion_disabled(self):
        assert_false(self.page.can_delete_files)

    def test_can_add_contributors(self):
        assert_false(self.page.can_add_contributors)

    def test_remove_contributors(self):
        assert_false(self.page.can_remove_contributors)

    def test_edit_wiki(self):
        assert_false(self.page.can_edit_wiki)

    def test_watermarked_background(self):
        assert_equal(
            1,
            len(
                self.page.driver.find_elements_by_css_selector(
                    'div.watermarked'
                )
            ),
        )


class FromProject(Create, ProjectRegistrationFixture):
    pass


class FromSubproject(Create, SubprojectRegistrationFixture):
    pass