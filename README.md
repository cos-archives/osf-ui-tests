OSF-UI-Tests
============

### OSF user interface smoke tests with Selenium as the tool of choice.

### Selenium test suites broken down into test specific areas i.e.:
* User account creation tests 
* --or--
* Project dashboard tests
    
### These test suites are composed of individual tests i.e.:
* Try to create a user without a password
* --or--
* Try to create a user with a short password

### Guidelines for adding tests
* Factor common functions into util.py
* Put database info (user names, project titles) in config.py
* Make sure that all database entries created during tests are cleared during teardown
