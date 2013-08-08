import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

# Project imports
import base
import util
import config


class ProjectRenameTests(base.ProjectSmokeTest):


    def test_project_rename(self):
        """
        test to make sure that rename a project works correctly
        """

        util.project_rename(self.driver, "NewProject")

        # refresh page and assert change was made
        project_name = self.driver.find_element_by_id("node-title-editable").text
        self.assertEqual(project_name, "NewProject")

        #cleanup
        util.project_rename(self.driver, config.project_title)

# Generate tests
util.generate_tests(ProjectRenameTests)

# Run tests
if __name__ == '__main__':
    unittest.main()