"""
Configuration for smokescreen testing
"""

# Default time for WebDriver.implicitly_wait
selenium_wait_time = 5

# 
#osf_home = 'http://192.155.89.121'
osf_home = 'http://50.116.49.207'

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
