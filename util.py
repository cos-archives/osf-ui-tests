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

def goto_profile(driver):
    """
    goes to a logged in user's public profile

    Args:
        driver : selenium.webdriver instance
        username : OSF username
        password : OSF password
    """
    # go to OSF home page
    driver.get(config.osf_home)

    # grab the profile button and load the page
    profile_button = driver.find_element_by_link_text('My Public Profile')
    profile_button.click()


def goto_project(driver, project_name):
    """
    goes to a logged in user's specific project

    Args:
        driver : selenium.webdriver instance
        project_name : name of project to be loaded (case sensitive)
    """
    # go to user's profile
    goto_profile(driver)

    # grab the project button and load the page
    project_button = driver.find_element_by_link_text(project_name)
    project_button.click()

def logout(driver):
    """
    logs current user out of OSF

    Args:
        driver : selenium.webdriver instance
    """

    # browse to OSF page
    driver.get(config.osf_home)

    # locate and click logout button
    driver.find_element_by_xpath('a[@href="/logout"]').click()

def create_project(driver, project_title, project_description):
    """Create new project

    Args:
        driver : selenium.webdriver instance
        project_title : project title
        project_description : project description
    Returns:
        URL of created project

    """

    # Browse to dashboard page
    driver.get('%s/dashboard' % (config.osf_home))

    #find the new project link and click it
    driver.find_element_by_link_text("New Project").click()

    # enter the title and description of your project
    # in the relevant fields and submit
    title_field = driver.find_element_by_xpath(
        '//form[@name="newProject"]//input[@id="title"]')
    description_field = driver.find_element_by_xpath(
        '//form[@name="newProject"]//textarea[@id="description"]')
    title_field.send_keys(project_title)
    description_field.send_keys(project_description)
    submit_button = driver.find_element_by_xpath(
        '//button[@class="btn primary"][@type="submit"]')
    submit_button.click()

    # Return project URL
    return driver.current_url

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
    client[config.db_name]['node'].remove({'title': title})
