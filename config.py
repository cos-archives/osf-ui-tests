"""
Configuration for smokescreen testing
"""

# 
osf_home = 'localhost:5000'

# 
mongo_uri = 'localhost:20771'
db_name = 'test'

# 
username = 'test@test.test'
password = 'testtest'

# 
registration_data = {
    'fullname' : 'test test',
    'username' : 'test@test.test',
    'username2' : 'test@test.test',
    'password' : 'testtest',
    'password2' : 'testtest',
}


second_user_registration_data = {
    'fullname' : 'test second',
    'username' : 'test@second.test',
    'username2' : 'test@second.test',
    'password' : 'testsecond',
    'password2' : 'testsecond',
}

# Test project data
project_title = 'test project'
project_description = 'test project description'
