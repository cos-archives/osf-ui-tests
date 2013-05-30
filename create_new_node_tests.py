import unittest

from selenium import webdriver
from pymongo import MongoClient

from util import login, create_project, clear_project

class create_new_node(unittest.TestCase):

    def setUp(self):
        username = "samson@gmail.com"
        password = "jeans123"
        self.driver = webdriver.Firefox()
        login(self.driver, username, password)
        self.url = create_project(
            self.driver, "Sam's Great Project", "This is a great project")

    def test_new_node(self):
        self.driver.get(self.url)
        create_node_btn = self.driver.find_element_by_link_text("New Node")
        create_node_btn.click()
        title_field = self.driver.find_element_by_xpath(
            '//form[@class="well form-inline"]//input[@name="title"]')
        title = "This is a node"
        title_field.send_keys(title)
        category_fields = self.driver.find_elements_by_xpath(
            '//form[@class="well form-inline"]//select[@id="select01"]')
        for field in category_fields:
            if field.text.find('Project'):
                field.click()
        submit_btn = self.driver.find_element_by_xpath(
            '//button[@class="btn"][@type="submit"]')
        submit_btn.click()
        self.assertEqual(self.driver.find_element_by_link_text(title).text, title)

    def tearDown(self):
        self.driver.close()
        clear_project("Sam's Great Project")

