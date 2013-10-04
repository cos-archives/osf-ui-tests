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

    # NOTE: This test only applies to subprojects
    @unittest.skip('known failure')
    def test_subproject_registration_parent_title(self):
        """ Verify that a registration's parent project title matches the
        original project """
        # As of 9 Sep 2013, registrations of subprojects do not preserve the
        # parent project in the header.
        self._test_registration_matches(
            page=self._subproject(),
            attribute='parent_title'
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

    @unittest.skip('known failure')
    def test_project_registration_logged(self):
        """ Project variant of ``self._test_registration_logged`` """
        # As of 9 Sep 2013, the log reads "component" here instead of "project"
        self._test_registration_logged(self._project())

    def test_subproject_registration_logged(self):
        """ Subproject variant of ``self._test_registration_logged`` """
        # TODO: This fails right now because a subproject is referred to as a
        # "node" in the log.
        self._test_registration_logged(self._subproject())