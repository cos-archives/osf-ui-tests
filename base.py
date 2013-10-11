"""
Base classes for smoke tests. Test classes can subclass various
classes defined here instead of repetitively defining setUp and 
tearDown methods. Note: these classes do NOT inherit from 
unittest.TestCase. If subclasses need to be detected by unittest / 
nose, they must multiply inherit from TestCase. This is done to 
permit abstract test classes that will not be detected by unittest /
nose.
"""

# Imports
from functools import wraps
import os
import shutil
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait

# Project imports
import config
import util
import os
import shutil
import tempfile
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wait
from pages.helpers import WaitForPageReload
from selenium.webdriver.common.action_chains import ActionChains


class SmokeTest(unittest.TestCase):
    """Base class for smoke tests. Creates a WebDriver
    on setUp and quits on tearDown.

    """
    # Allow multiprocessing for individual tests
    _multiprocess_can_split_ = True

    def setUp(self):
        
        # Launch Selenium using options specified as class
        # variables, which can include driver_name and
        # desired_capabilities
        if hasattr(self, 'driver_opts'):
            self.driver = util.launch_driver(**self.driver_opts)
        else:
            self.driver = util.launch_driver()

        self.site_root = config.osf_home.strip('/')
        
    def tearDown(self):
        
        # Quit Selenium
        # Note: Use WebDriver.quit() instead of WebDriver.close();
        # otherwise, SauceLabs tests will never finish
        self.driver.quit()

    def get_element(self, css):
        return wait(
            driver=self.driver,
            timeout=5
        ).until(
            method=ec.visibility_of_element_located(
                (By.CSS_SELECTOR, css)
            )
        )


class UserSmokeTest(SmokeTest):
    """Class for smoke tests that require user login.
    Creates a user and logs in on setUp and logs out on
    tearDown.

    """
    def setUp(self):
        
        # Call parent setUpClass
        super(UserSmokeTest, self).setUp()

        # Create user account and login
        self.user_data = util.create_user(self.driver)
        util.login(
            self.driver,
            self.user_data['username'],
            self.user_data['password']
        )

    def tearDown(self):
        
        # Log out
        util.logout(self.driver)

        # Call parent tearDown
        super(UserSmokeTest, self).tearDown()

    def create_user(self):
        return util.create_user(self.driver)

    def log_in(self, user=None):
        if not user:
            user = self.user_data
        return util.login(
            self.driver,
            user['username'],
            user['password']

        )

    def log_out(self):
        return util.logout(self.driver)

    def get_user_url(self):
        util.goto_profile(self.driver)
        user_url=self.driver.find_element_by_css_selector("tr>td>a:first-child").get_attribute("href")
        util.goto_project(self.driver)
        return user_url

        
class ProjectSmokeTest(UserSmokeTest):
    """Class for smoke tests that require project
    creation. Creates a project on setUp and deletes it
    on tearDown.

    """
    def setUp(self):
        
        # Call parent setUp
        super(ProjectSmokeTest, self).setUp()

        # Create test project
        self.project_url = util.create_project(self.driver)
    
        # Browse to project page
        util.goto_project(self.driver)

        # add file paths
        self.image_files = _generate_full_filepaths({
            'jpg': 'test.jpg',
            'png': 'test.png',
            'gif': 'test.gif',
        })

        self.text_files = _generate_full_filepaths({
            'txt': 'txtfile.txt',
            'html': 'htmlfile.html',
        })

        self.archive_files = _generate_full_filepaths({
            'tar': 'text_files.tar',
            'tar.gz': 'text_files.tar.gz',
            'zip': 'text_files.zip',
        })
        self.archive_file_contents = ('txtfile.txt','htmlfile.html')

        self.binary_files = _generate_full_filepaths({
            'pdf': 'pdffile.pdf',
        })

        self.versioned_files = _generate_full_filepaths({
            0: 'versioned-0.txt',
            1: 'versioned-1.txt',
        })
    
    def tearDown(self):
        
        # Delete test project
        #util.delete_project(self.driver)

        # Call parent tearDown
        super(ProjectSmokeTest, self).tearDown()

    def goto(self, page, *args, **kwargs):
        """Go to a project's page

        :param page: The name of the destination page. Acceptable include
            "files", "settings", and "registrations"
        :param node_url: Optional. The URL of the project or component to use.

        :returns: True on success, KeyError page
        """
        base_url = kwargs.get('node_url', self.project_url).strip('/')

        build_path = {
            'dashboard': lambda: base_url,
            'files': lambda: '/'.join([base_url, 'files']),
            'file': lambda: '/'.join([base_url, 'files', args[0]]),
            'registrations': lambda: '/'.join([base_url, 'registrations']),
            'settings': lambda: '/'.join([base_url, 'settings']),
            'user-dashboard': lambda: '/'.join([self.site_root, 'dashboard']),
            'wiki': lambda: '/'.join([base_url, 'wiki']),
        }

        # This will throw a KeyError if the page type is not in the above dict.
        self.driver.get(
            url=build_path[page]()
        )

    # Node methods

    def add_contributor(self, user):
        # click the "add" link
        self.get_element('#contributors a[href="#addContributors"]').click()

        # enter the user's email address
        self.get_element('div#addContributors input[type=text]').send_keys(
            user['username']
        )

        # click the search button
        self.get_element('#addContributors button').click()

        # click the radio button for the first result
        self.get_element('#addContributors input[type=radio]').click()

        # click the "Add" button
        self.get_element('#addContributors button.btn.primary').click()

    def remove_contributor(self, user_data):
        # mouse over to the contribute's name
        element_to_hover_over \
            = self.get_element('#contributors a[data-fullname="'
                               + user_data["fullname"]+'"]')
        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()

        # click the remove icon
        element_to_hover_over.find_element_by_css_selector("i").click()

        self.driver.switch_to_alert().accept()

    def get_log(self):

        log_entry_element = self.get_element("div.span5 dl")

        class LogEntry(object):
            def __init__(self, log_element):
                entry_element = log_element.find_element_by_css_selector('dd:nth-of-type(1)')

                self.log_text = entry_element.text

                self.log_url=[]
                css_url = entry_element.find_elements_by_css_selector('a')
                for x in css_url:
                    self.log_url.append(x.get_attribute('href'))

                self.log_time = datetime.strptime(
                    log_element.find_element_by_css_selector("dt:nth-of-type(1)").text,
                    "%m/%d/%y %I:%M %p",
                )

        return LogEntry(log_entry_element)

    def edit_title(self, text):

        self.get_element('#node-title-editable').click()

        # select the name field on the new popup
        edit_profile_name_field = self.get_element(
            'div.popover-content input.span2'
        )

        # delete the current project name
        edit_profile_name_field.clear()

        # enter the new project name
        edit_profile_name_field.send_keys(text)

        # find and click submit new project name
        self.get_element(
            'div.popover-content button.btn.btn-primary'
        ).click()

    def set_permission(self, permission, url=None):

        url = url or self.project_url
        url = url.strip('/')

        self.driver.get('{url}/permissions/{prm}'.format(
            url=url,
            prm=permission,
        ))

    def make_private(self, url=None):
        """Make a project or component private.

        :param url: Optional. The URL of the project or component - defaults to
            ``self.project_url``
        """

        url = url or self.project_url

        if self.is_public(url):
            self.set_permission('private', url)

    def make_public(self, url=None):
        """Make a project or component private.

        :param url: Optional. The URL of the project or component - defaults to
            ``self.project_url``
        """

        url = url or self.project_url

        if not self.is_public(url):
            self.set_permission('public', url)

    def is_public(self, url=None):
        """Test whether a project or component is public.

        :param url: Optional. The URL of the project of component to test.
            Defaults to ``self.project_url``

        :return: ``True`` if public; ``False`` if private
        """
        url = url or self.project_url

        self.driver.get(url)

        state = self.get_element(
            '.btn-toolbar .btn-group:first-child button.disabled'
        ).text.lower()

        return state == 'public'

    def add_versioned_file(self):
        filename = 'versioned.txt'
        upload_dir = os.path.dirname(self.text_files['txt']['path'])
        f = os.path.join(upload_dir, filename)

        # rename and upload version 0.
        shutil.copy(self.versioned_files[0]['path'], f)
        self.add_file(f)

        # rename and upload version 1
        shutil.copy(self.versioned_files[1]['path'], f)
        self.add_file(f)

        # delete the temp file
        os.remove(f)

        return filename

    def add_file(self, path, node_url=None):
        """Add a file. Assumes that the test class is harnessed to a project"""
        node_url = node_url or self.project_url
        self.goto('files', node_url=node_url)

        self.driver.execute_script('''
            $('input[type="file"]').offset({left : 50});
        ''')

        # Find file input
        field = self.driver.find_element_by_css_selector('input[type=file]')

        # Enter file into input
        field.send_keys(path)

        # Upload files
        self.driver.find_element_by_css_selector(
            'div.fileupload-buttonbar button.start'
        ).click()

    # Component methods

    def add_component(self, component_type, name, project_url=None):
        """Adds a component to the current project

        :param component_type: a string representing the component type
        :param name: the new component's name

        :returns: URL of the component"""

        # go to the project
        self.goto(
            'dashboard',
            project_url or self.project_url
        )

        # click "Add Component"
        self.get_element('a.btn[href="#newComponent"]').click()

        modal = self.get_element('div.modal.fade.in')

        # enter the component name
        modal.find_element_by_css_selector(
            'input[name="title"]'
        ).send_keys(name)

        # choose the component type
        modal.find_element_by_css_selector(
            'select#category'
        ).send_keys(component_type)

        # click OK
        modal.find_element_by_css_selector(
            '.modal-footer button[type="submit"]'
        ).click()

        # return url of the component
        return self.get_element(
            '#Nodes li.project:last-child h3 a'
        ).get_attribute('href')

    def delete_component(self, url, project=None):
        """Deletes the component.

        Assumes that you are logged in as a user with contributor access to the
        parent project.

        :param url: URL of the project to delete
        :param project: Optional. The URL of the project from which to delete
            the component.
        """
        raise NotImplementedError

    def assert_error_page(self, error_msg, url=None):
        """Optionally navigate to page, then check for provided error
        message.

        :param error_msg: Error message
        :param url: Optional URL

        """
        # if a url was provided, go there
        if url:
            self.driver.get(url)

        # an alert should be present with the error message
        self.assertIn(
            error_msg,
            self.get_element('div.span12 h2').text,
        )

    def assert_not_found(self, url=None):

        self.assert_error_page('Page not found.', url)

    def assert_not_authorized(self, url=None):
        """Navigate to the page, and see if the item is accessible.
        """

        self.assert_error_page('Unauthorized.', url)

    def assert_forbidden(self, url=None):
        """Nav  igate to the resource and verify the 403 (Forbidden) error is
        present.
        """

        self.assert_error_page('Forbidden.', url)

    def create_fork(self, url=None):
        """Create a fork, and return its URL

        :param url: Optional. The URL of the component or project to fork
        """

        if url:
            self.driver.get(url)

        with WaitForPageReload(self.driver):
            # click the fork button
            self.get_element(
                'div.btn-toolbar div.btn-group:last-child a:last-child'
            ).click()

        return self.driver.current_url

    def create_registration(
            self,
            registration_type='Open-Ended Registration',
            node_url=None,
    ):
        """Create a new registration.

        Args:
            registration_type : Type of registration
            registration_data : Data for registration form
        Returns:
            URL of registration
        """
        # Browse to registrations page
        node_url = node_url or self.project_url
        if registration_type == 'Open-Ended Registration':
            self.driver.get(
                node_url.strip('/') + '/register/Open-Ended_Registration'
            )
        elif registration_type == 'OSF-Standard Pre-Data Collection Registration':
            self.driver.get('/'.join([
                node_url.strip('/'),
                'register',
                'OSF-Standard_Pre-Data_Collection_Registration',
            ]))
        else:
            raise ValueError('Invalid registration type')

        # Fill out the form
        self.get_element(
            'textarea.ember-view'
        ).send_keys('Test content for a textarea.')

        for elem in self.driver.find_elements_by_css_selector(
                'div#registration_template select'):
            elem.send_keys('Yes')


        self.get_element(
            'form.form-horizontal div.control-group input.ember-view'
        ).send_keys('continue')

        self.get_element('div.ember-view button.btn.primary').click()

        # Hack: Wait for registration label so that we can get the
        # correct URL for the registration
        self.get_element('.label-important')

        # Return URL of registration
        return self.driver.current_url

    def _file_exists_in_project(self, filename):
        """Goes to a file's page, verifies by checking the title."""
        self.goto('file', filename)

        return filename in self.get_element('div.page-header h1').text

    def _generate_full_filepaths(self, file_dict):
        """Given a dict of filenames, return a dict that includes the full path
        for each."""
        # Make each filename a full path
        for f in file_dict:
            file_dict[f] = {
                'path': os.path.join(  # append filename to this directory
                    os.path.dirname(os.path.abspath(__file__)),
                    'upload_files',
                    file_dict[f]),
                'filename': file_dict[f],
        }

        return file_dict

    def _assert_time(self,time_now):
        #assert the time
        time_diff = abs(datetime.utcnow()-time_now)
        self.assertTrue(time_diff < timedelta(minutes=2))

    def _add_wiki(self,text):
        #help function to add the wiki "text"
        util.edit_wiki(self.driver)
        util.clear_wiki_text(self.driver)
        util.add_wiki_text(self.driver, text)
        util.submit_wiki_text(self.driver)

    def get_wiki_text(self):
        """Provided you are on a wiki page, get the raw contents of the page"""
        return self.driver.execute_script('''
            return $('textarea#wmd-input').val()
        ''')

    def set_wiki_text(self, text, append=True):
        textarea = self.get_element('textarea#wmd-input')

        if not append:
            # clear the input
            self.driver.execute_script('''
                $('textarea#wmd-input').val('')
            ''')

        textarea.send_keys(text)





def not_implemented(f):
    @wraps(f)
    @unittest.skip('Not yet implemented')
    def wrapper(*args, **kwargs):
        return f
    return wrapper


def _generate_full_filepaths(file_dict):
    """Given a dict of filenames, return a dict that includes the full path
    for each."""
    # Make each filename a full path
    for f in file_dict:
        file_dict[f] = {
            'path': os.path.join(  # append filename to this directory
                os.path.dirname(os.path.abspath(__file__)),
                'upload_files',
                file_dict[f]),
            'filename': file_dict[f],
        }

    return file_dict
