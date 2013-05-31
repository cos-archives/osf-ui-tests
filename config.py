"""
Configuration for smokescreen testing
"""

# Default time for WebDriver.implicitly_wait
selenium_wait_time = 5

# 
osf_home = 'localhost:5000'

# 
mongo_uri = 'localhost:20771'
db_name = 'test'

# 
registration_data = {
    'fullname' : 'test test',
    'username' : 'test@test.test',
    'username2' : 'test@test.test',
    'password' : 'testtest',
    'password2' : 'testtest',
}

# Test project data
project_title = 'test project'
project_description = 'test project description'
