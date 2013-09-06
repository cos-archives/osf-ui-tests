import datetime as dt
import unittest

from pages import helpers, ProjectPage, LoginPage


class RegistrationTests(unittest.TestCase):
    _project = lambda x: helpers.get_new_project('New Project')

    def _subproject(self):
        return self._project().add_component(
            title='New Subproject',
            component_type='Project',
        )

    def _test_registration_template(self, page):

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
        self._test_registration_template(self._project())

    def test_project_registration_template(self):
        self._test_registration_template(self._subproject())

    def _test_registration_meta(self, page):
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
        self._test_registration_meta(self._project())

    def test_subproject_registration_meta(self):
        self._test_registration_meta(self._subproject())

    def _test_registration_list(self, page):
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
        registrations = self._test_registration_list(page=self._project())

        self.assertEqual(len(registrations), 1)

    def test_subproject_registration_listed(self):
        registrations = self._test_registration_list(page=self._subproject())

        self.assertEqual(len(registrations), 1)

    def test_project_registration_list_title(self):
        page = self._project()
        title = page.title
        registrations = self._test_registration_list(page)

        self.assertEqual(
            registrations[0].title,
            title
        )

    def test_subproject_registration_list_title(self):
        page = self._subproject()
        title = page.title
        registrations = self._test_registration_list(page)

        self.assertEqual(
            registrations[0].title,
            title
        )

    def test_project_registration_list_date(self):
        page = self._project()
        date_created = page.date_created
        registrations = self._test_registration_list(page)

        self.assertAlmostEqual(
            registrations[0].date,
            date_created,
            delta=dt.timedelta(minutes=2)
        )

    def test_subproject_registration_list_date(self):
        page = self._subproject()
        date_created = page.date_created
        registrations = self._test_registration_list(page)

        self.assertAlmostEqual(
            registrations[0].date,
            date_created,
            delta=dt.timedelta(minutes=2)
        )

    def _test_registration_matches(self, page, attribute):
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
        self._test_registration_matches(
            page=self._project(),
            attribute='title'
        )

    def test_subproject_registration_title(self):
        self._test_registration_matches(
            page=self._subproject(),
            attribute='title'
        )

    def test_subproject_registration_parent_title(self):
        self._test_registration_matches(
            page=self._subproject(),
            attribute='parent_title'
        )

    def test_project_registration_components_empty(self):
        self._test_registration_matches(
            page=self._project(),
            attribute='component_names'
        )

    def test_project_registration_components(self):
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
        self._test_registration_matches(
            page=self._project(),
            attribute='contributors'
        )

    def test_subproject_registration_contributors(self):
        self._test_registration_matches(
            page=self._subproject(),
            attribute='contributors'
        )

    def test_project_registration_created_date(self):
        self._test_registration_matches(
            page=self._project(),
            attribute='date_created'
        )

    def test_subproject_registration_created_date(self):
        self._test_registration_matches(
            page=self._subproject(),
            attribute='date_created'
        )

    def test_project_registration_last_updated_date(self):
        self._test_registration_matches(
            page=self._project(),
            attribute='last_updated'
        )

    def test_subproject_registration_last_updated_date(self):
        self._test_registration_matches(
            page=self._subproject(),
            attribute='last_updated'
        )

    def test_project_registration_wiki_home(self):
        page = self._project()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            page=page,
            attribute='wiki_home_content'
        )

    def test_subproject_registration_wiki_home(self):
        page = self._subproject()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            page=page,
            attribute='wiki_home_content'
        )

    def test_project_registration_log_matches(self):
        self._test_registration_matches(
            page=self._project(),
            attribute='logs',
        )

    def test_subproject_registration_log_matches(self):
        self._test_registration_matches(
            page=self._subproject(),
            attribute='logs',
        )

    def _test_registration_logged(self, page):
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
        """ When a project is registered, the action should be in its log."""
        self._test_registration_logged(self._project())

    def test_subproject_registration_logged(self):
        """ When a subproject is registered, the action should be in its log."""
        # TODO: This fails right now because a subproject is referred to as a
        # "node" in the log.
        self._test_registration_logged(self._subproject())