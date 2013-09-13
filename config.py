"""
Configuration for smokescreen testing
"""

# Default time for WebDriver.implicitly_wait
selenium_wait_time = 5

# Domain to use for all tests.
osf_home = 'https://staging.openscienceframework.org'

# make sure there is no trailing slash.
osf_home = osf_home.rstrip('/')

# raise an exception if the root domain is production.
if '/openscienceframwork.org' in osf_home:
    raise Exception(
        'OSF UI tests should *never* be run against production. '
        '(A large number of database entries and files are generated '
        'during testing.)'
    )

# Test project data
project_title = 'test project'
project_description = 'test project description'

node_title = 'test node'

open_ended_registration_data = {
    'div#registration_template textarea' : 'test registration',
    'div.container form input[type=text].ember-text-field' : 'continue',
}

osf_standard_registration_data = {
    # The first select on the form
    '#registration_template div.control-group:first-child select' : 'Yes',
    # The second select on the form (immediate sibling of the first select)
    '#registration_template div.control-group:first-child + div.control-group select' : 'No',
    '#registration_template textarea' : 'None',
    'div.container form input[type=text].ember-text-field' : 'continue',
}

#

from selenium import webdriver

def make_remote_opts(capabilities, platform=None, version=None, name=None):
    
    # Freeze local variables
    _locals = locals()
    
    desired_capabilities = capabilities.copy()
    desired_capabilities.update({
        key : _locals[key] for key in _locals
            if _locals[key] is not None
    })

    return {
        'driver_name' : 'Remote',
        'desired_capabilities' : desired_capabilities,
    }  

nodes = [
    {'driver_name' : 'Firefox'},
    #make_remote_opts(webdriver.DesiredCapabilities.CHROME, 'OS X 10.6'),
    #make_remote_opts(webdriver.DesiredCapabilities.CHROME, 'Windows 8'),
    #make_remote_opts(webdriver.DesiredCapabilities.CHROME, 'Linux'),
]
