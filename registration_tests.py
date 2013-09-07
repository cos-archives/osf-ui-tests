import datetime as dt
import unittest

from pages import helpers


class RegistrationTests(unittest.TestCase):
    """This test case is for testing the act of creating a registration, and
    consistency between a registration and its original node.
    """

    def _project(self):
        """ Create and return a top-level project.

        The ``current_url`` of the driver is the project's overview.
        """
        return helpers.get_new_project('New Project')

    def _subproject(self):
        """ Create and return a project which is the child of a project.

        The ``current_url`` of the driver is the project's overview.
        """
        return self._project().add_component(
            title='New Subproject',
            component_type='Project',
        )

    def _test_registration_template(self, page):
        """ Given a project, register it and verify that the registration
        template's name is displayed in the header.
        """

        meta = ('sample narrative', )
        template = 'Open-Ended Registration'

        page = page.add_registration(
            registration_type=template,
            meta=meta,
        )

        self.assertEqual(
            page.registration_template,
            template,
        )

        page.close()

    def test_project_registration_template(self):
        """ Project variant of ``self._test_registration_template`` """
        self._test_registration_template(self._project())

    def test_subproject_registration_template(self):
        """ Subproject variant of ``self._test_registration_template`` """
        self._test_registration_template(self._subproject())

    def _test_registration_meta(self, page):
        """ Given a project, register it and verify that the registration's meta
         information is correct.
        """
        meta = ('sample narrative', )

        page = page.add_registration(
            registration_type='Open-Ended Registration',
            meta=meta
        )

        self.assertEqual(
            page.registration_meta,
            meta
        )

        page.close()

    def test_project_registration_meta(self):
        """ Project variant of ``self._test_registration_meta`` """
        self._test_registration_meta(self._project())

    def test_subproject_registration_meta(self):
        """ Subproject variant of ``self._test_registration_meta`` """
        self._test_registration_meta(self._subproject())

    def _test_registration_list(self, page):
        """ Given a project, register it and verify that the new registration is
         in the project's registration list
        """
        _url = page.driver.current_url

        page = page.add_registration(
            registration_type='Open-Ended Registration',
            meta=('sample narrative', )
        )

        page.driver.get(_url)

        self.assertEqual(len(page.registrations), 1)

        r = page.registrations

        page.close()

        return r

    def test_project_registration_listed(self):
        """ After registering a project, the registration should be listed in
         the project's Registrations pane. """
        registrations = self._test_registration_list(page=self._project())

        self.assertEqual(len(registrations), 1)

    def test_subproject_registration_listed(self):
        """ Subproject variant of ``self.test_project_registration_listed`` """
        registrations = self._test_registration_list(page=self._subproject())

        self.assertEqual(len(registrations), 1)

    def _test_registration_list_title(self, page):
        """ Given a project, register it and verify that that registration in
         the project's registration list has the correct title.
        """
        title = page.title
        registrations = self._test_registration_list(page)

        self.assertEqual(
            registrations[0].title,
            title
        )

    def test_project_registration_list_title(self):
        """ Project variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(self._project())

    def test_subproject_registration_list_title(self):
        """ Subproject variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(self._subproject())

    def _test_registration_list_date(self, page):
        """ Given a project, register it and verify that the registration in
         the project's registration list has the correct date.
        """
        date_created = page.date_created
        registrations = self._test_registration_list(page)

        self.assertAlmostEqual(
            registrations[0].date,
            date_created,
            delta=dt.timedelta(minutes=2)
        )

    def test_project_registration_list_date(self):
        """ Project variant of ``self._test_registration_list_date`` """
        self._test_registration_list_date(self._project())

    def test_subproject_registration_list_date(self):
        """ Subproject variant of ``self._test_registration_list_date``
        """
        self._test_registration_list_date(self._subproject())

    def _test_registration_matches(self, page, attribute):
        """ Given a project, register it and verify that the attribute provided
         matches between the project and its registration.

         Note that the value of the project's attribute is stored before the
         project is registered, as the act of registration may otherwise change
         the state - for example, the registration of a project should include
         its log *before* the project was registered, while the project's log
         should immediately be updated to include the creation of the
         registration.
        """
        parent_value = getattr(page, attribute)

        page = page.add_registration(
            registration_type='Open-Ended Registration',
            meta=('sample narrative', )
        )

        self.assertEqual(
            getattr(page, attribute),
            parent_value,
        )

        page.close()

    def test_project_registration_title(self):
        """ Verify that a registration's title matches the original project """
        self._test_registration_matches(
            page=self._project(),
            attribute='title'
        )

    def test_subproject_registration_title(self):
        """ Subproject variant of ``self._test_project_registration_title`` """
        self._test_registration_matches(
            page=self._subproject(),
            attribute='title'
        )

    # NOTE: This test only applies to subprojects
    def test_subproject_registration_parent_title(self):
        """ Verify that a registration's parent project title matches the
        original project """
        self._test_registration_matches(
            page=self._subproject(),
            attribute='parent_title'
        )

    def test_project_registration_components_empty(self):
        """ Verify that a registration's (empty) component list matches the
        original project"""
        self._test_registration_matches(
            page=self._project(),
            attribute='component_names'
        )

    def test_subproject_registration_components_empty(self):
        """ Subproject variant of
        ``self._test_project_registration_components_empty``
        """
        self._test_registration_matches(
            page=self._subproject(),
            attribute='component_names'
        )

    def test_project_registration_components(self):
        """ Verify that a registration's (non-empty) component list matches the
        original project """

        page = self._project()

        # add component
        page = page.add_component(
            title='Test Component',
            component_type='Other',
        )

        page = page.parent_project()

        # add a subproject
        page = page.add_component(
            title='Test Subproject',
            component_type='Project',
        )

        page = page.parent_project()

        self._test_registration_matches(
            page=page,
            attribute='component_names'
        )

    def test_subproject_registration_components(self):
        """ Subproject variant of ``self._test_project_registration_components``
        """
        page = self._project()

        page = page.add_component(
            title='Subproject',
            component_type='Project',
        )

        # add component
        page = page.add_component(
            title='Test Component',
            component_type='Other',
        )

        page = page.parent_project()

        self._test_registration_matches(
            page=page,
            attribute='component_names'
        )

    def test_project_registration_contributors(self):
        """ Verify that a registration's contributor list matches the original
        project """

        self._test_registration_matches(
            page=self._project(),
            attribute='contributors'
        )

    def test_subproject_registration_contributors(self):
        """ Subproject variant of
        ``self._test_project_registration_contributors``
        """
        self._test_registration_matches(
            page=self._subproject(),
            attribute='contributors'
        )

    def test_project_registration_created_date(self):
        """ Verify that a registration's creation date matches the original
        project
        """
        self._test_registration_matches(
            page=self._project(),
            attribute='date_created'
        )

    def test_subproject_registration_created_date(self):
        """ Subproject variant of
        ``self._test_project_registration_created_date``
        """
        self._test_registration_matches(
            page=self._subproject(),
            attribute='date_created'
        )

    def test_project_registration_last_updated_date(self):
        """ Verify that a registration's last updated date matches the original
        project """
        self._test_registration_matches(
            page=self._project(),
            attribute='last_updated'
        )

    def test_subproject_registration_last_updated_date(self):
        """ Subproject variant of
        ``self._test_project_registration_updated_date``
        """
        self._test_registration_matches(
            page=self._subproject(),
            attribute='last_updated'
        )

    def test_project_registration_wiki_home(self):
        """ Verify that a registration's wiki homepage content matches the
        original project """
        page = self._project()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            page=page,
            attribute='wiki_home_content'
        )

    def test_subproject_registration_wiki_home(self):
        """ Subproject variant of ``self._test_project_registration_wiki_home``
        """
        page = self._subproject()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            page=page,
            attribute='wiki_home_content'
        )

    def test_project_registration_log_matches(self):
        """ Verify that a registration's log matches the original project """
        self._test_registration_matches(
            page=self._project(),
            attribute='logs',
        )

    def test_subproject_registration_log_matches(self):
        """ Subproject variant of
        ``self._test_project_registration_log_matches``
        """
        self._test_registration_matches(
            page=self._subproject(),
            attribute='logs',
        )

    def _test_registration_logged(self, page):
        """ Given a project, register it and verify that the action appears in
        the original project's logs.
        """
        user = page.contributors[0].full_name

        _url = page.driver.current_url

        page = page.add_registration(
            registration_type='Open-Ended Registration',
            meta=('test narrative', )
        )

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            u'{user} registered project {title}'.format(
                user=user,
                title=page.title
            )
        )

        page.close()

    def test_project_registration_logged(self):
        """ Project variant of ``self._test_registration_logged`` """
        self._test_registration_logged(self._project())

    def test_subproject_registration_logged(self):
        """ Subproject variant of ``self._test_registration_logged`` """
        # TODO: This fails right now because a subproject is referred to as a
        # "node" in the log.
        self._test_registration_logged(self._subproject())