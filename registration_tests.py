import datetime as dt
import unittest

from pages import helpers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    def _test_registration_list(self, regi_type, page):
        """ Given a project, register it and verify that the new registration is
         in the project's registration list
        """
        _url = page.driver.current_url
        if regi_type == 1:
            page = page.add_registration(
                registration_type='Open-Ended Registration',
                meta=('sample narrative', )
            )
        elif regi_type == 2:
            page = page.add_registration(
                registration_type='OSF-Standard Pre-Data Collection Registration',
                meta=('No', 'No', 'sample narrative', )
            )
        elif regi_type == 3:
            page = page.add_registration(
                registration_type='Replication Recipe (Brandt et al., 2013): Pre-Registration',
                meta=('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                      'no', 'j', 'k', 'l', 'm', 'n', 'o',
                      'Exact', 'Close', 'Different', 'Exact', 'Close', 'Different', 'Exact', 'p', 'q',
                      'r', 's', 't',)
            )
        elif regi_type == 4:
            page = page.add_registration(
                registration_type='Replication Recipe (Brandt et al., 2013): Post-Completion',
                meta=('u',
                      'v', 'w', 'significantly different from the original effect size', 'inconclusive', 'x', 'y', 'z', '1',)
            )

        page.driver.get(_url)

        self.assertEqual(len(page.registrations), 1)

        r = page.registrations

        page.close()

        return r

    def test_project_registration_listed_type1(self):
        """ After registering a project, the registration should be listed in
         the project's Registrations pane. """
        registrations = self._test_registration_list(
            regi_type=1,
            page=self._project(),
        )

        self.assertEqual(len(registrations), 1)

    def test_subproject_registration_listed_type1(self):
        """ Subproject variant of ``self.test_project_registration_listed`` """
        registrations = self._test_registration_list(
            regi_type=1,
            page=self._subproject()
        )

        self.assertEqual(len(registrations), 1)

    def test_project_registration_listed_type2(self):
        """ After registering a project, the registration should be listed in
         the project's Registrations pane. """
        registrations = self._test_registration_list(
            regi_type=2,
            page=self._project(),
        )

        self.assertEqual(len(registrations), 1)

    def test_subproject_registration_listed_type2(self):
        """ Subproject variant of ``self.test_project_registration_listed`` """
        registrations = self._test_registration_list(
            regi_type=2,
            page=self._subproject()
        )

        self.assertEqual(len(registrations), 1)

    def test_project_registration_listed_type3(self):
        """ After registering a project, the registration should be listed in
         the project's Registrations pane. """
        registrations = self._test_registration_list(
            regi_type=3,
            page=self._project(),
        )

        self.assertEqual(len(registrations), 1)

    def test_subproject_registration_listed_type3(self):
        """ Subproject variant of ``self.test_project_registration_listed`` """
        registrations = self._test_registration_list(
            regi_type=3,
            page=self._subproject()
        )

        self.assertEqual(len(registrations), 1)

    def test_project_registration_listed_type4(self):
        """ After registering a project, the registration should be listed in
         the project's Registrations pane. """
        registrations = self._test_registration_list(
            regi_type=4,
            page=self._project(),
        )

        self.assertEqual(len(registrations), 1)

    def test_subproject_registration_listed_type4(self):
        """ Subproject variant of ``self.test_project_registration_listed`` """
        registrations = self._test_registration_list(
            regi_type=4,
            page=self._subproject()
        )

        self.assertEqual(len(registrations), 1)

    def _test_registration_list_title(self, regi_type, page):
        """ Given a project, register it and verify that that registration in
         the project's registration list has the correct title.
        """
        title = page.title
        registrations = self._test_registration_list(regi_type, page)

        self.assertEqual(
            registrations[0].title,
            title
        )

    def test_project_registration_list_title_type1(self):
        """ Project variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(1, self._project())

    def test_subproject_registration_list_title_type1(self):
        """ Subproject variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(1, self._subproject())

    def test_project_registration_list_title_type2(self):
        """ Project variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(2, self._project())

    def test_subproject_registration_list_title_type2(self):
        """ Subproject variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(2, self._subproject())

    def test_project_registration_list_title_type3(self):
        """ Project variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(3, self._project())

    def test_subproject_registration_list_title_type3(self):
        """ Subproject variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(3, self._subproject())

    def test_project_registration_list_title_type4(self):
        """ Project variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(4, self._project())

    def test_subproject_registration_list_title_type4(self):
        """ Subproject variant of ``self._test_registration_list_title``
        """
        self._test_registration_list_title(4, self._subproject())

    def _test_registration_list_date(self, regi_type, page):
        """ Given a project, register it and verify that the registration in
         the project's registration list has the correct date.
        """
        date_created = page.date_created
        registrations = self._test_registration_list(regi_type, page)

        self.assertAlmostEqual(
            registrations[0].date,
            date_created,
            delta=dt.timedelta(minutes=2)
        )

    def test_project_registration_list_date_type1(self):
        """ Project variant of ``self._test_registration_list_date`` """
        self._test_registration_list_date(1, self._project())

    def test_subproject_registration_list_date_type1(self):
        """ Subproject variant of ``self._test_registration_list_date``
        """
        self._test_registration_list_date(1, self._subproject())

    def test_project_registration_list_date_type2(self):
        """ Project variant of ``self._test_registration_list_date`` """
        self._test_registration_list_date(2, self._project())

    def test_subproject_registration_list_date_type2(self):
        """ Subproject variant of ``self._test_registration_list_date``
        """
        self._test_registration_list_date(2, self._subproject())

    def test_project_registration_list_date_type3(self):
        """ Project variant of ``self._test_registration_list_date`` """
        self._test_registration_list_date(3, self._project())

    def test_subproject_registration_list_date_type3(self):
        """ Subproject variant of ``self._test_registration_list_date``
        """
        self._test_registration_list_date(3, self._subproject())

    def test_project_registration_list_date_type4(self):
        """ Project variant of ``self._test_registration_list_date`` """
        self._test_registration_list_date(4, self._project())

    def test_subproject_registration_list_date_type4(self):
        """ Subproject variant of ``self._test_registration_list_date``
        """
        self._test_registration_list_date(4, self._subproject())

    def _test_registration_matches(self, regi_type, page, attribute):
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

        if regi_type == 1:
            page = page.add_registration(
                registration_type='Open-Ended Registration',
                meta=('sample narrative', )
            )
        elif regi_type == 2:
            page = page.add_registration(
                registration_type='OSF-Standard Pre-Data Collection Registration',
                meta=('No', 'No', 'sample narrative', )
            )
        elif regi_type == 3:
            page = page.add_registration(
                registration_type='Replication Recipe (Brandt et al., 2013): Pre-Registration',
                meta=('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                      'no', 'j', 'k', 'l', 'm', 'n', 'o',
                      'Exact', 'Close', 'Different', 'Exact', 'Close', 'Different', 'Exact', 'p', 'q',
                      'r', 's', 't',)
            )
        elif regi_type == 4:
            page = page.add_registration(
                registration_type='Replication Recipe (Brandt et al., 2013): Post-Completion',
                meta=('u',
                      'v', 'w', 'significantly different from the original effect size', 'inconclusive', 'x', 'y', 'z', '1',)
            )

        WebDriverWait(page.driver, 8).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'html body DIV.watermarked DIV.container DIV.alert.alert-info')
            )
        )
        self.assertEqual(
            getattr(page, attribute),
            parent_value,
        )

        page.close()

    # NOTE: This test only applies to subprojects
    def test_subproject_registration_parent_title_type1(self):
        """ Verify that a registration's parent project title matches the
        original project """
        # As of 9 Sep 2013, registrations of subprojects do not preserve the
        # parent project in the header.
        self._test_registration_matches(
            regi_type=1,
            page=self._subproject(),
            attribute='parent_title'
        )

    def test_project_registration_wiki_home_type1(self):
        """ Verify that a registration's wiki homepage content matches the
        original project """
        page = self._project()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            regi_type=1,
            page=page,
            attribute='wiki_home_content'
        )

    def test_subproject_registration_wiki_home_type1(self):
        """ Subproject variant of ``self._test_project_registration_wiki_home``
        """
        page = self._subproject()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            regi_type=1,
            page=page,
            attribute='wiki_home_content'
        )

    # NOTE: This test only applies to subprojects
    def test_subproject_registration_parent_title_type2(self):
        """ Verify that a registration's parent project title matches the
        original project """
        # As of 9 Sep 2013, registrations of subprojects do not preserve the
        # parent project in the header.
        self._test_registration_matches(
            regi_type=2,
            page=self._subproject(),
            attribute='parent_title'
        )

    def test_project_registration_wiki_home_type2(self):
        """ Verify that a registration's wiki homepage content matches the
        original project """
        page = self._project()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            regi_type=2,
            page=page,
            attribute='wiki_home_content'
        )

    def test_subproject_registration_wiki_home_type2(self):
        """ Subproject variant of ``self._test_project_registration_wiki_home``
        """
        page = self._subproject()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            regi_type=2,
            page=page,
            attribute='wiki_home_content'
        )

    # NOTE: This test only applies to subprojects
    def test_subproject_registration_parent_title_type3(self):
        """ Verify that a registration's parent project title matches the
        original project """
        # As of 9 Sep 2013, registrations of subprojects do not preserve the
        # parent project in the header.
        self._test_registration_matches(
            regi_type=3,
            page=self._subproject(),
            attribute='parent_title'
        )

    def test_project_registration_wiki_home_type3(self):
        """ Verify that a registration's wiki homepage content matches the
        original project """
        page = self._project()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            regi_type=3,
            page=page,
            attribute='wiki_home_content'
        )

    def test_subproject_registration_wiki_home_type3(self):
        """ Subproject variant of ``self._test_project_registration_wiki_home``
        """
        page = self._subproject()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            regi_type=3,
            page=page,
            attribute='wiki_home_content'
        )

    # NOTE: This test only applies to subprojects
    def test_subproject_registration_parent_title_type4(self):
        """ Verify that a registration's parent project title matches the
        original project """
        # As of 9 Sep 2013, registrations of subprojects do not preserve the
        # parent project in the header.
        self._test_registration_matches(
            regi_type=4,
            page=self._subproject(),
            attribute='parent_title'
        )

    def test_project_registration_wiki_home_type4(self):
        """ Verify that a registration's wiki homepage content matches the
        original project """
        page = self._project()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            regi_type=4,
            page=page,
            attribute='wiki_home_content'
        )

    def test_subproject_registration_wiki_home_type4(self):
        """ Subproject variant of ``self._test_project_registration_wiki_home``
        """
        page = self._subproject()

        page.set_wiki_content('Test wiki content!')

        self._test_registration_matches(
            regi_type=4,
            page=page,
            attribute='wiki_home_content'
        )