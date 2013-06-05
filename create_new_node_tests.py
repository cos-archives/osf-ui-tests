"""

"""

import unittest

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Project imports
import base
import util
import config

class CreateNewNodeTest(base.ProjectSmokeTest):

    def test_create_node(self):

        # Create node
        util.create_node(self.driver)

        # Test node title
        self.assertEqual(
            self.driver.find_element_by_link_text(config.node_title).text, 
            config.node_title
        )

# Run tests
if __name__ == '__main__':
    unittest.main()
