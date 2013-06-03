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
 
### Issues: 
* Testing file submission with Selenium. Currently using blueimp. See page for issue: https://github.com/blueimp/jQuery-File-Upload/issues/1228 
Possible workrounds include: use requests to submit post request or via javascipt.

### Next steps:
* Finish file upload/deletion testing.
* Create registration tests
* Create add/delete contributer tests
* Move testing to Sauce Labs

### Notes: If issues arise during tests, look at the following suites first.
* user_creations_tests
* project_creation_tests
* utils -- relies heavily on the aforementioned test suites.
