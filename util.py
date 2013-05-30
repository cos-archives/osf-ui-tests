"""
Miscellaneous utility functions for smokescreen tests
"""

# Project imports
import config

# Set up MongoDB
from pymongo import MongoClient
client = MongoClient(config.mongo_uri)

def fill_form(form, fields):
    """Fill out form fields and click submit button.

    Args:
        form : webdriver element
        fields : dict of id -> value pairs for form

    """
    
    # Enter field values
    for field in fields:
        form.find_element_by_id(field).send_keys(fields[field])
    
    # Click submit button
    form.find_element_by_xpath('.//button[@type="submit"]').click()

def login(driver, login_data):
    """Login to OSF

    Args:
        driver : selenium.webdriver instance
        login_data : dict of id -> value pairs for login form

    Examples:
        > login(driver, {'username' : 'test@test.test', 'password' : 'testtest'})

    """
    
    # Browse to OSF page
    driver.get(config.osf_home)

    # Click login button
    driver.find_element_by_xpath('//a[@href="/account"]').click()
    
    # Get login form
    login_form = driver.find_element_by_xpath('//form[@name="signin"]')
    fill_form(login_form, login_data)

def create_user(driver, registration_data=config.registration_data):
    """Create a new user account.

    Args:
        driver : selenium.webdriver instance
        registration_data : dict of id -> value pairs for registration form
                            default: config.registration_data

    Examples:
        > create_user(driver, {
            'fullname' : 'test test',
            'username' : 'test@test.com',
            'username2' : 'test@test.com',
            'password' : 'testtest',
            'password2' : 'testtest',
        }

    """
    
    # Browse to account page
    driver.get('%s/account' % (config.osf_home))
    
    # Find form
    registration_form = driver.find_element_by_xpath('//form[@name="registration"]')
    
    # Fill out form
    fill_form(registration_form, registration_data)

def clear_user(username):
    """Clear user from database

    Args:
        username : Username

    """
    
    client[config.db_name]['user'].remove({'username' : username})

def clear_project(title):
    """Clear project from database

    Args:
        title : Project title

    """
    
    client[config.db_name]['node'].remove({'title' : title})
