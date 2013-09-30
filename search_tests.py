import unittest

import sunburnt

from pages import helpers
import config

solr = sunburnt.SolrInterface(config.solr_home)


class SearchSecurity(unittest.TestCase):
    def setUp(self):
#        solr.delete_all()
#        solr.commit()
        self.page = helpers.get_new_project('Top Project')

    def tearDown(self):
        self.page.close()

    def test_project_security(self):
        # Projects are private by default. There should be none in the index.

        self.assertEqual(0, projects_in_solr())

        self.page.public = True

        # Now there should be one project
        self.assertEqual(1, projects_in_solr())

        self.page.public = False

        # After setting it back to private, the index should be empty.
        self.assertEqual(0, projects_in_solr())

    def test_subproject_security(self):
        project_url = self.page.driver.current_url
        project_id = self.page.id
        self.page = self.page.add_component('Subproject', 'Project')
        subproject_url = self.page.driver.current_url
        subproject_id = self.page.id
        # project and subproject private
        self.assertFalse(is_project_in_solr(project_id))
        self.assertFalse(is_project_in_solr(subproject_id))

        self.page.driver.get(subproject_url)
        self.page.public = True
        # project private; subproject public
        self.assertFalse(is_project_in_solr(project_id))
        self.assertTrue(is_project_in_solr(subproject_id))

        # project public; subproject public
        self.page.driver.get(project_url)
        self.page.public = True
        self.assertTrue(is_project_in_solr(project_id))
        self.assertTrue(is_project_in_solr(subproject_id))

        # project public; subproject private
        self.page.driver.get(subproject_url)
        self.page.public = False
        self.assertTrue(is_project_in_solr(project_id))
        self.assertFalse(is_project_in_solr(subproject_id))


def projects_in_solr():
    return len(solr.query(category='project').execute())


def is_project_in_solr(project_id):
    r = solr.query(category='project').execute()
    for p in r:
        if p.get(project_id + '_title'):
            return True
    return False


def debug():
    r = solr.query().execute()
    from pprint import pprint
    [pprint(x) for x in r]