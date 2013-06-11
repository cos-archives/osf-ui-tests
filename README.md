OSF-UI-Tests
============

### OSF user interface smoke tests with Selenium as the tool of choice.

### Selenium test suites broken down into test specific areas i.e.:
* User account creation tests 
* --or--
* Project dashboard tests
    
### These test suites are composed of individual tests, e.g.:
* Try to create a user without a password
* --or--
* Try to create a user with a short password

### Guidelines for adding tests
* Factor common functions into util.py
* Put database info (user names, project titles) in config.py
* Make sure that all database entries created during tests are cleared during teardown

### Environment variables
* SAUCE_USERNAME
* SAUCE_ACCESS_KEY

### Running the tests
* From localhost
    * Point config:osf_home to localhost:5000
    * Start mongod
    * Start OSF (main.py)
    * Start Sauce Connect
        * https://saucelabs.com/docs/connect
* From development server
    * Point config:osf_home to dev URL
* To run the tests
    * Run one test file: python <testfile.py> or nosetests <testfile.py>
    * Run all test files: nosetests
    * Run all test files using multiple cores: nosetests --processes=2
 
### Notes: If issues arise during tests, look at the following suites first.
* user_creations_tests
* project_creation_tests
* utils -- relies heavily on the aforementioned test suites.
