"""
Configuration for smokescreen testing
"""

# Default time for WebDriver.implicitly_wait
selenium_wait_time = 5

# 
osf_home = 'http://192.155.89.121'
#osf_home = 'localhost:5000'

# 
mongo_uri = 'localhost:20771'
db_name = 'test'

# Test project data
project_title = 'test project'
project_description = 'test project description'

node_title = 'test node'

open_ended_registration_data = {
    '#ember295' : 'test registration',
    '#ember319' : 'continue',
}

osf_standard_registration_data = {
    '#ember299' : 'Yes',
    '#ember454' : 'No',
    '#ember587' : 'None',
    '#ember610' : 'continue',
}
