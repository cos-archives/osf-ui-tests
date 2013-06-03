"""
Miscellaneous utility functions for smokescreen tests
"""

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# Project imports
import config

# Set up MongoDB
from pymongo import MongoClient

client = MongoClient(config.mongo_uri)

def get_alert_boxes(driver, alert_text):
    """Check page for alert boxes. Asserts that there is exactly
    one matching alert.

    Args:
        driver : WebDriver instance
        alert_text : Text to search for in alert box
    Returns:
        matching alert boxes

    """

    # Find alerts
    alerts = driver.find_elements_by_xpath(
        '//*[text()[contains(translate(., "%s", "%s"), "%s")]]' % \
            (alert_text.upper(), alert_text.lower(), alert_text.lower())
    )

    # Return matching alert boxes
    return alerts

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

def login(driver, username=config.registration_data['username'], password=config.registration_data['password']):
    """Login to OSF

    Args:
        driver : selenium.webdriver instance
        login_data : dict of id -> value pairs for login form

    Examples:
        > login(driver, {'username' : 'test@test.test', 'password' : 'testtest'})

    """

    # Browse to OSF login page
    driver.get('%s/account' % (config.osf_home))

    # Get login form
    login_form = driver.find_element_by_xpath('//form[@name="signin"]')
    fill_form(login_form, {
        'username' : username,
        'password' : password,
    })

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

def goto_dashboard(driver):

    #
    driver.get('%s/dashboard' % (config.osf_home))

def goto_profile(driver):
    """
    goes to a logged in user's public profile

    Args:
        driver : selenium.webdriver instance
        username : OSF username
        password : OSF password
    """
    # go to OSF home page
    goto_dashboard(driver)

    # grab the profile button and load the page
    driver.find_element_by_link_text('My Public Profile').click()

def goto_project(driver, project_title=config.project_title):
    """goes to a logged in user's specific project

    Args:
        driver : selenium.webdriver instance
        project_title : name of project to be loaded (case sensitive)

    """
    # go to user's profile
    goto_dashboard(driver)

    # grab the project button and load the page
    driver.find_element_by_link_text(project_title).click()
    return driver.current_url

def goto_settings(driver, project_name):

    # Browse to project page
    goto_project(driver, project_name)

    # Click Settings button
    driver.find_element_by_link_text('Settings').click()

def delete_project(driver, project_title=config.project_title):
    """Delete a project. Note: There is no confirmation for
    project deletion as of this writing, but should be soon.

    Args:
        driver : webdriver
        project_title : project title

    """

    # Browse to project settings
    goto_settings(driver, project_title)

    # Click Delete button
    driver.find_element_by_xpath('//button[@type="submit"]').click()

def logout(driver):
    """logs current user out of OSF

    Args:
        driver : selenium.webdriver instance

    """

    # browse to OSF page
    driver.get(config.osf_home)

    # locate and click logout button
    driver.find_element_by_xpath('//a[@href="/logout"]').click()

def create_project(driver, project_title=config.project_title, project_description=config.project_description):
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
        '//form[@name="newProject"]//input[@id="title"]'
    )
    description_field = driver.find_element_by_xpath(
        '//form[@name="newProject"]//textarea[@id="description"]'
    )
    title_field.send_keys(project_title)
    description_field.send_keys(project_description)
    submit_button = driver.find_element_by_xpath(
        '//button[@class="btn primary"][@type="submit"]')
    submit_button.click()

    # Return project URL
    return driver.current_url

def make_project_public(driver, url):

    driver.get(url)
    link = driver.find_element_by_link_text("Make public")
    link.click()
    time.sleep(3) #wait until modal box finishes moving
    driver.find_element_by_xpath('//button[contains(@class, "modal-confirm")]').click()
    return driver.current_url

def make_project_private(driver, url):

    driver.get(driver.current_url)
    link = driver.find_element_by_link_text("Make private")
    link.click()
    time.sleep(3) #wait until modal box finishes moving
    driver.find_element_by_xpath('//button[contains(@class, "modal-confirm")]').click()
    return driver.current_url

def clear_user(username=config.registration_data['username']):
    """Clear user from database

    Args:
        username : Username

    """

    client[config.db_name]['user'].remove({'username' : username})

def clear_project(title=config.project_title):
    """Clear project from database

    Args:
        title : Project title

    """
    client[config.db_name]['node'].remove({'title': title})

def _edit_wiki(driver):

    edit_button = driver.find_element_by_link_text('Edit')
    edit_button.click()

def _get_wiki_input(driver):

    return driver.find_element_by_id('wmd-input')

def _add_wiki_text(driver, text):

    _get_wiki_input(driver).send_keys(text)

def _submit_wiki_text(driver):
    """ Click submit button. """

    driver.find_element_by_xpath(
        '//div[@class="wmd-panel"]//input[@type="submit"]'
    ).click()

def _get_wiki_par(driver):
    """ Get <p> containing wiki text. """

    # Set implicitly_wait to short value: text may not
    # exist, so we don't want to wait too long to find it
    driver.implicitly_wait(0.1)

    # Extract wiki text
    # Hack: Wiki text element isn't uniquely labeled,
    # so find its sibling first
    try:
        wiki_par = driver.find_element_by_xpath(
            '//div[@id="addContributors"]/following-sibling::div//p'
        )
    except NoSuchElementException:
        wiki_par = None

    # Set implicitly_wait to original value
    driver.implicitly_wait(config.selenium_wait_time)

    # Return element
    return wiki_par

def _get_wiki_text(driver):
    """ Get text from wiki <p>. """

    # Get <p> containing wiki text
    wiki_par = _get_wiki_par(driver)

    # Extract text
    if wiki_par is not None:
        return wiki_par.text
    return ''

def select_partial(driver, id, start, stop):
    """Select a partial range of text from an element.

    Args:
    driver : WebDriver instance
    id : ID of target element
    start : Start position
    stop : Stop position

    """
    # Inject partial selection function
    # Adapted from http://stackoverflow.com/questions/646611/programmatically-selecting-partial-text-in-an-input-field
    driver.execute_script('''
        (function(field, start, end) {
        if( field.createTextRange ) {
        var selRange = field.createTextRange();
        selRange.collapse(true);
        selRange.moveStart('character', start);
        selRange.moveEnd('character', end-start);
        selRange.select();
        } else if( field.setSelectionRange ) {
        field.setSelectionRange(start, end);
        } else if( field.selectionStart ) {
        field.selectionStart = start;
        field.selectionEnd = end;
        }
        field.focus();
        })(document.getElementById("%s"), %d, %d);
        ''' % (id, start, stop))
