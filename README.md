OSF-UI-Tests
============

### OSF user interface tests

### Current State

Our UI tests to this point do not require access to the OSF codebase; but to a
running instance of the OSF. This allows them to be run against a dev or staging
server instead of only on the developer's local machine.

One of the challenges we've faced is that of keeping our UI tests current with
the OSF. With the introduction of unit and functional tests within the main OSF
repo, we plan to alleviate this by eventually moving all tests there. To prepare
for this, we're cleaning up our tests to use the page object pattern and a set
of fixtures representing user actions.

### Tools

#### Nose

Nose offers several benefits, many of which we're not yet utilizing. As the nose
test runner completely supports `unittest`-based tests, there should be few
issues supporting legacy tests while we migrate to use node more fully.

####solr

Solr is written in Java and runs as a standalone full-text search server within a 
servlet container such as Jetty. Solr uses the Lucene Java search library at its 
core for full-text indexing and search, and has REST-like HTTP/XML and JSON APIs 
that make it easy to use from virtually any programming language. Solr's powerful 
external configuration allows it to be tailored to almost any type of application 
without Java coding, and it has an extensive plugin architecture when more advanced 
customization is required.

#### Selenium

Selenium is a tool designed to allow the develop to drive a web browser with
code, emulating user behavior. The biggest challenge in doing so has so far been
with respect to timing - sensing page refreshes, particularly those driven by
clicking a button or executing Javascript.

We've attempted to alleviate this by moving to the page object pattern. A page
object represents an individual page of the OSF, exposing properties and methods
corresponding to elements on the page and actions that the user might take.

### Guidelines for adding tests

New tests should whenever possible be added to an existing test suite. If you're
testing that registrations of a project have a description that matches that of
their parent projects, `/tests/registrations/test_create.py` already contains
a test class that creates a project and registers it as appropriate. Since no
action is taken in the browser to perform these tests, the registration is
created only once, saving significant time.

Use the assertion methods in `nose.tools`, instead of those provided by
`unittest`. These are PEP8-compliant.

### Running the tests
* From localhost
    * Point config:osf_home to localhost:5000
    * Start mongod
    * invoke solr
    * Start OSF (main.py)
* From development server
    * Point config:osf_home to dev URL
* To run the tests
    * Run one test file: nosetests <testfile.py>
    * Run all test files: nosetests

### Using Sauce

*section pending*
