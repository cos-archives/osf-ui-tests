"""
Miscellaneous utility functions for smokescreen tests
"""
import uuid
import time

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Project imports
import config

def launch_driver(driver_name='Firefox', wait_time=config.selenium_wait_time):
    """Create and configure a WebDriver.
    
    Args:
        driver_name : Name of WebDriver to use
        wait_time : Time to implicitly wait for element load

    """
        
    # Start WebDriver
    # If driver_name is a method of webdriver, use that; 
    # else use webdriver.Firefox()
    if hasattr(webdriver, driver_name):
        driver = getattr(webdriver, driver_name)()
    else:
        driver = webdriver.Firefox()

    # Wait for elements to load
    driver.implicitly_wait(wait_time)
    
    # Return driver
    return driver

def clear_text(elm):
    """Clear text via backspace. Usually we can skip
    this and clear via elm.clear() directly, but this
    doesn't work in all cases (e.g. Wiki editing).

    """
    
    for _ in range(len(elm.text)):
        elm.send_keys(Keys.BACK_SPACE)

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

def login(driver, username, password):
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

def gen_user_data(_length=12):
    """ Generate data to create a user account. """
    
    fullname = str(uuid.uuid1())[:_length]
    username = str(uuid.uuid1())[:_length] + '@osftest.org'
    password = str(uuid.uuid1())[:_length]

    username2 = username
    password2 = password
    
    _locs = locals()
    return {k:_locs[k] for k in _locs if not k.startswith('_')}

def create_user(driver, user_data=None):
    """Create a new user account.

    Args:
        driver : selenium.webdriver instance
        user_data : dict of id -> value pairs for registration form
                    default: config.registration_data
    Returns:
        dict of user information

    Examples:
        > create_user(driver, {
            'fullname' : 'test test',
            'username' : 'test@test.com',
            'username2' : 'test@test.com',
            'password' : 'testtest',
            'password2' : 'testtest',
        }

    """
    if user_data is None:
        user_data = gen_user_data()

    # Browse to account page
    driver.get('%s/account' % (config.osf_home))

    # Find form
    registration_form = driver.find_element_by_xpath('//form[@name="registration"]')

    # Fill out form
    fill_form(registration_form, user_data)
    
    # Return user data
    return user_data

def goto_dashboard(driver):

    """Browse to dashboard page.
    
    Args:
        driver : WebDriver instance

    """
    driver.get('%s/dashboard' % (config.osf_home))

def goto_profile(driver):
    """Browse to public profile page. 
    
    Args:
        driver : WebDriver instance
    
    """
    # Browse to dashboard
    goto_dashboard(driver)

    # Click Public Profile link
    driver.find_element_by_link_text('My Public Profile').click()

def goto_project(driver, project_title=config.project_title):

    """Browse to project page.

    Args:
        driver : WebDriver instance
        project_title : Title of project to be loaded
    Returns:
        URL of project page

    """
    # Browse to dashboard
    goto_dashboard(driver)

    # Click on project title
    driver.find_element_by_link_text(project_title).click()
    return driver.current_url

def goto_settings(driver, project_name):
    """Browse to project settings page.

    Args:
        driver : WebDriver instance
        project_name : Project name

    """
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
    """ Log out of OSF.

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
    # Browse to dashboard
    goto_dashboard(driver)

    # Click New Project button
    driver.find_element_by_link_text("New Project").click()

    # Fill out form and submit
    project_form = driver.find_element_by_xpath('//form[@name="newProject"]')
    fill_form(
        project_form, {
            'title' : project_title,
            'description' : project_description,
        }
    )

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


def edit_wiki(driver):

    edit_button = driver.find_element_by_link_text('Edit')
    edit_button.click()

def get_wiki_input(driver):

    return driver.find_element_by_id('wmd-input')

def add_wiki_text(driver, text):

    get_wiki_input(driver).send_keys(text)

def submit_wiki_text(driver):
    """ Click submit button. """

    driver.find_element_by_xpath(
        '//div[@class="wmd-panel"]//input[@type="submit"]'
    ).click()

def get_wiki_par(driver):
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

def get_wiki_text(driver):
    """ Get text from wiki <p>. """

    # Get <p> containing wiki text
    wiki_par = get_wiki_par(driver)

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