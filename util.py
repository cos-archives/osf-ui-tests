"""
Miscellaneous utility functions for smokescreen tests
"""

# Project imports
import config

# Set up MongoDB
from pymongo import MongoClient
client = MongoClient(config.mongo_uri)

def login(driver, username, password):
    """Log in to OSF

    Args:
        driver : selenium.webdriver instance
        username : OSF username
        password : OSF password
    """
    
    # Browse to OSF page
    driver.get(config.osf_home)

    # Click login button
    login_link = driver.find_element_by_xpath('//a[@href="/account"]')
    login_link.click()

    # Get login elements
    signin_email = driver.find_element_by_xpath('//form[@name="signin"]//input[@id="username"]')
    signin_password = driver.find_element_by_xpath('//form[@name="signin"]//input[@id="password"]')
    signin_submit = driver.find_element_by_xpath('//form[@name="signin"]//button[@type="submit"]')
    
    # Login
    signin_email.send_keys(username)
    signin_password.send_keys(password)
    signin_submit.click()

def clear_users():
    """Clear all users from database

    """
    
    client[config.db_name]['user'].remove()

def clear_project(title):
    """Clear project from database

    Args:
        title : Project title

    """
    
    client[config.db_name]['node'].remove({'title' : title})
