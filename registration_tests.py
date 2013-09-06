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