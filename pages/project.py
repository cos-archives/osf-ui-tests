import datetime as dt
import urlparse
from collections import namedtuple

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as exc
from selenium.webdriver.common.keys import Keys


import config
import logs
from generic import ApiKey, OsfPage
from helpers import WaitForFileUpload, WaitForPageReload


class NodePage(OsfPage):
    """Base class for Component and Project pages. In other words, anything that
    is represented as a ``Node`` model in the backend.

    It should not be instantiated directly.
    """

    def __init__(self, *args, **kwargs):
        super(NodePage, self).__init__(*args, **kwargs)

    def _verify_page(self):
        """ Return True if the current page is the one expected for a
        ``NodePage``."""
        return (
            len(self.driver.find_elements_by_id('node-title-editable')) == 1 or
            len(self.driver.find_elements_by_id('node-title')) == 1
        )

    @property
    def contributors(self):
        """ A list of contributors for the node, parsed from the
        header.

        :returns: [``Contributor``, ...]
        """
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#contributors a[href^="/profile"]')
            )
        )

        # TODO: This doesn't take into account non-registered users.
        C = namedtuple('Contributor', ('full_name', 'profile_url', 'id'))

        return [
            C(
                full_name=x.text,
                profile_url=x.get_attribute('href'),
                id=x.get_attribute('href').split('/')[-1],
            )
            for x in self.driver.find_elements_by_css_selector(
                '#contributors a[href^="/profile"]'
            )
        ]

    @property
    def can_add_contributors(self):
        if len(self.driver.find_elements_by_css_selector(
                '#contributors > a[href="#addContributors"]'
        )) == 0:
            return False

        return True

    @property
    def can_remove_contributors(self):
        element_to_hover_over = self.driver.find_element_by_css_selector(
            '#contributors span.contributor a')
        ActionChains(
            self.driver
        ).move_to_element(element_to_hover_over).perform()

        # click the remove icon
        return bool(
            len(element_to_hover_over.find_elements_by_css_selector("i"))
        )

    def add_multi_contributor(self, user1, user2):

        # click the "add" link
        self.driver.find_element_by_css_selector(
            '#contributors a[href="#addContributors"]'
        ).click()

        # wait for the modal to be visible
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.ID, 'addContributors')
            )
        )

        # enter the user1's email address
        self.driver.find_element_by_css_selector(
            'div#addContributors input[data-bind="value:query"]'
        ).send_keys(user1.email)

        # click the search button
        self.driver.find_element_by_css_selector(
            '#addContributors button.btn'
        ).click()
         # wait for a result to display
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#addContributors a.btn.contrib-button')
            )
        )

        # click the radio button for the first result
        self.driver.find_element_by_css_selector(
            '#addContributors a.btn.contrib-button'
        ).click()

        self.driver.find_element_by_css_selector(
            'div#addContributors input[data-bind="value:query"]'
        ).clear()

        # enter the user1's email address
        self.driver.find_element_by_css_selector(
            'div#addContributors input[data-bind="value:query"]'
        ).send_keys(user2.email)

        # click the search button
        self.driver.find_element_by_css_selector(
            '#addContributors button.btn'
        ).click()

        # wait for a result to display
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#addContributors a.btn.contrib-button')
            )
        )

        # click the radio button for the first result
        self.driver.find_element_by_css_selector(
            '#addContributors a.btn.contrib-button'
        ).click()

        with WaitForPageReload(self.driver):

            # click the "Add" button
            self.driver.find_element_by_css_selector(
                '#addContributors a[data-bind="click:submit"]'
            ).click()

    def add_multi_contributor_delete(self, user1, user2):

        # click the "add" link
        self.driver.find_element_by_css_selector(
            '#contributors a[href="#addContributors"]'
        ).click()

        # wait for the modal to be visible
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.ID, 'addContributors')
            )
        )

        # enter the user1's email address
        self.driver.find_element_by_css_selector(
            'div#addContributors input[data-bind="value:query"]'
        ).send_keys(user1.email)

        # click the search button
        self.driver.find_element_by_css_selector(
            '#addContributors button.btn'
        ).click()
         # wait for a result to display
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#addContributors a.btn.contrib-button')
            )
        )

        # click the radio button for the first result
        self.driver.find_element_by_css_selector(
            '#addContributors a.btn.contrib-button'
        ).click()

        self.driver.find_element_by_css_selector(
            'div#addContributors input[data-bind="value:query"]'
        ).clear()

        # enter the user1's email address
        self.driver.find_element_by_css_selector(
            'div#addContributors input[data-bind="value:query"]'
        ).send_keys(user2.email)

        # click the search button
        self.driver.find_element_by_css_selector(
            '#addContributors button.btn'
        ).click()

        # wait for a result to display
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#addContributors a.btn.contrib-button')
            )
        )

        # click the radio button for the first result
        self.driver.find_element_by_css_selector(
            '#addContributors a.btn.contrib-button'
        ).click()

        self.driver.find_elements_by_css_selector(
            "#addContributors A.btn.btn-default.contrib-button"
        )[0].click()

        with WaitForPageReload(self.driver):

            # click the "Add" button
            self.driver.find_element_by_css_selector(
                '#addContributors a[data-bind="click:submit"]'
            ).click()

    def remove_contributor(self, user):
        # mouse over to the contribute's name
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#contributors a[data-fullname="' + user.full_name+'"]'
                )
            )
        )
        element_to_hover_over = self.driver.find_element_by_css_selector(
            '#contributors a[data-fullname="' + user.full_name+'"]'
        )
        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()

        # click the remove icon
        element_to_hover_over.find_element_by_css_selector("i").click()

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div.modal-dialog button[class='btn btn-primary']"
                )
            )
        )

        self.driver.find_element_by_css_selector(
            "div.modal-dialog button[class='btn btn-primary']"
        ).click()

    def add_contributor(self, user):

        # click the "add" link
        self.driver.find_element_by_css_selector(
            '#contributors a[href="#addContributors"]'
        ).click()

        # wait for the modal to be visible
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.ID, 'addContributors')
            )
        )

        # enter the user's email address
        self.driver.find_element_by_css_selector(
            'div#addContributors input[data-bind="value:query"]'
        ).send_keys(user.email)

        # click the search button
        self.driver.find_element_by_css_selector(
            '#addContributors button.btn'
        ).click()

        # wait for a result to display
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#addContributors a.btn.contrib-button')
            )
        )

        # click the radio button for the first result
        self.driver.find_element_by_css_selector(
            '#addContributors a.btn.contrib-button'
        ).click()

        with WaitForPageReload(self.driver):

            # click the "Add" button
            self.driver.find_element_by_css_selector(
                '#addContributors a[data-bind="click:submit"]'
            ).click()

    @property
    def date_created(self):
        """ The date the node was created, parsed from the header.

        :returns: ``datetime.datetime``
        """
        date_string = self.driver.find_elements_by_css_selector(
            '#contributors span.date')[0].text

        return dt.datetime.strptime(date_string, '%Y/%m/%d %I:%M %p')

    @property
    def last_updated(self):
        """ When the node was last updated, parsed from the header.

        :returns: ``datetime.datetime``
        """
        date_string = self.driver.find_elements_by_css_selector(
            '#contributors span.date')[1].text

        return dt.datetime.strptime(date_string, '%Y/%m/%d %I:%M %p')

    @property
    def id(self):
        """The node's ID, parsed from the URL.

        :returns: ``str``
        """
        return urlparse.urlparse(
            self.driver.current_url
        ).path.strip('/').split('/')[-1]

    @property
    def parent_id(self):
        """The node's parent's ID, parsed from the URL."""
        pcs = urlparse.urlparse(
            self.driver.current_url
        ).path.strip('/').split('/')
        if len(pcs) < 4:
            return None
        return pcs[1]

    @property
    def title(self):
        """The node's title, parsed from the header

        :returns: ``str``
        """
        return self.driver.find_element_by_css_selector('h1.node-title').text

    @title.setter
    def title(self, value):
        self.driver.find_element_by_id('node-title-editable').click()

        textbox = self.driver.find_element_by_css_selector(
            'div.editable-popover input[type="text"]'
        )
        textbox.clear()
        textbox.send_keys(value)

        with WaitForPageReload(self.driver):
            self.driver.find_element_by_css_selector(
                'div.editable-popover button[type="submit"]'
            ).click()

    @property
    def tag(self):
        """The node's title, parsed from the header

        :returns: ``str``
        """
        return self._tag

    def add_tag(self, value):

        textbox = self.driver.find_element_by_css_selector(
            'INPUT#node-tags_tag'
        )
        textbox.send_keys(value+'\n')

    @property
    def watched(self):
        """Whether the user is watching the node

        :returns: ``bool``
        """
        return 'Unwatch' in self.driver.find_element_by_id('watchCount').text

    @watched.setter
    def watched(self, value):
        if self.watched == value:
            return

        self.driver.find_element_by_id('watchCount').click()

        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element(
                (By.ID, 'watchCount'),
                'Unwatch' if value else 'Watch',
            )
        )


    @property
    def num_watchers(self):
        """Number of watchers on the node

        :returns: ``int``
        """
        return int(self.driver.find_element_by_id('watchCount').text.split(' ')[1])

    @property
    def description(self):
        try:
            return self.driver.find_element_by_css_selector(
                '.node-description'
            ).text
        except exc.NoSuchElementException:
            return None

    @property
    def forked_from_url(self):
        try:
            return self.driver.find_element_by_css_selector(
                'a.node-forked-from'
            ).get_attribute('href')
        except exc.TimeoutException:
            return None

    @property
    def parent_title(self):
        """The node's parent's title, parsed from the header.

        :returns: ``str`` or ``None``
        """
        try:
            return self.driver.find_element_by_css_selector(
                '#node-title a'
            ).text
        except exc.NoSuchElementException:
            return None


    @property
    def parent_link(self):
        """The URL of the node's parent, parsed from the header.

        :returns: ``str`` or ``None``
        """
        return self.driver.find_element_by_css_selector(
            '.node-parent-title a'
        ).get_attribute('href')

    @property
    def _tag(self):
        """The node's tag element.

        :returns: ``WebElement``
        """
        return self.driver.find_element_by_css_selector('span.tag').text

    @property
    def components(self):
        """The node's list of components, parsed from the dashboard

        :returns: [``Component``, ... ]
        """
        C = namedtuple('Component', ['title', 'url'])
        components = []
        for elem in self.driver.find_elements_by_css_selector('#Nodes h3 a'):
            components.append(
                C(
                    title=elem.text,
                    url=elem.get_attribute('href')
                )
            )

        return components

    @property
    def component_names(self):
        """ The names of the node's components

         :returns: (``str``, )
        """
        return tuple([x.title for x in self.components])

    @property
    def public(self):
        return (
            'disabled' in
            self.driver.find_element_by_css_selector(
                '#overview div.btn-group:nth-of-type(1) > :nth-child(2)'
            ).get_attribute('class')
        )

    @public.setter
    def public(self, value):
        if self.public == value:
            return

        # If public, the "Make private" element will be the only <a>.
        # If private, the opposite is true.
        self.driver.find_element_by_css_selector(
            '#overview div.btn-group:nth-of-type(1) > a'
        ).click()

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.modal.fade.in button.btn-primary')
            )
        )

        confirm_button = self.driver.find_element_by_css_selector(
            'div.modal.fade.in button.btn-primary'
        )

        WebDriverWait(self.driver, 1).until(
            EC.visibility_of(confirm_button)
        )

        with WaitForPageReload(self.driver):
            confirm_button.click()

    @property
    def settings(self):
        self.driver.get(
            self.driver.find_element_by_link_text(
                'Settings'
            ).get_attribute('href')
        )
        return NodeSettingsPage(driver=self.driver)

    def parent_project(self):
        """Navigate to the nodes's parent project.

        :returns: ``ProjectPage``
        """
        if self.parent_link:
            self.driver.get(self.parent_link)
            return ProjectPage(driver=self.driver)
        else:
            # TODO: This doesn't seem like the right exception to raise.
            raise AttributeError("No parent project found.")

    @property
    def can_edit_wiki(self):
        _url = self.driver.current_url

        self.driver.get(
            self.driver.find_element_by_link_text(
                'Wiki').get_attribute('href') + 'home/'
        )

        edit_button_class = self.driver.find_elements_by_css_selector(
            'ul.nav-pills'
        )[1].find_element_by_link_text('Edit').get_attribute('class')

        self.driver.get(_url)

        return not 'disabled' in edit_button_class

    def set_wiki_content(self, content, page='home'):
        """Sets the content of a wiki page.

        :param content: string to be set as the page's content.
        :param page: Optional. The wiki page to set. Defaults to "home"
        """
        _url = self.driver.current_url

        self.driver.get(
            self.driver.find_element_by_link_text(
                'Wiki').get_attribute('href') + '{}/edit/'.format(page)
        )

        # clear existing input
        self.driver.execute_script("$('#wmd-input').val('');")

        # set the new content
        self.driver.find_element_by_id('wmd-input').send_keys(content)

        # submit it
        self.driver.find_element_by_css_selector(
            '.wmd-panel input[type="submit"]'
        ).click()

        # Go back to the project page.
        self.driver.get(_url)

    def get_wiki_content(self, page='home'):
        """ Get the content of a wiki page.

        :param page: Optional. Defaults to "home".

        :returns: ``str``
        """
        _url = self.driver.current_url

        self.driver.get(
            '{}/wiki/{}'.format(
                _url.strip('/'),
                page
            )
        )

        # set the new content
        content = self.driver.execute_script(
            'var e = $("#addContributors + div");'
            'e.find("> div:first-child").remove();'
            'return e.text()'
        ).strip()

        # Go back to the project page.
        self.driver.get(_url)

        return content

    @property
    def wiki_home_content(self):
        """The content of the wiki "home" page"""
        return self.get_wiki_content()

    @property
    def registrations(self):
        """The node's list of registrations, parsed from the registrations pane.

         :returns: [``Registration``, ...]
        """
        # Click "Registrations"
        self.driver.find_element_by_css_selector(
            '#overview div.subnav'
        ).find_element_by_link_text(
            'Registrations'
        ).click()

        R = namedtuple('Registration', ('title', 'url', 'date'))

        registrations = []

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'ul.list-group li.project h3')
            )
        )

        # for each list entry
        for r in self.driver.find_elements_by_css_selector(
            'ul.list-group li.project h3'
        ):
            registrations.append(
                # build the Registration instance
                R(
                    title=r.find_element_by_css_selector('a').text,
                    url=r.find_element_by_css_selector('a').get_attribute(
                        'href'
                    ),
                    date=dt.datetime.strptime(
                        r.text.split('Registered: ')[-1],
                        '%m/%d/%y %I:%M %p'
                    ),
                )
            )

        return registrations

    @property
    def forks(self):
        """The noe's list of forks, parsed from the forks pane.

         :returns: [``Fork``, ... ]
        """
        forks = []
        # Click "Forks"
        self.driver.find_element_by_css_selector(
            '#overview div.subnav'
        ).find_element_by_link_text(
            'Forks'
        ).click()

        F = namedtuple('Fork', ('title', 'url'))

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'ul.list-group li#projects-widget.project.list-group-item h3'
                )
            )
        )

        # for each list entry
        for f in self.driver.find_elements_by_css_selector(
            'ul.list-group li#projects-widget.project.list-group-item h3'
        ):
            forks.append(
                # build the Registration instance
                F(
                    title=f.find_element_by_css_selector('a').text,
                    url=f.find_element_by_css_selector('a').get_attribute(
                        'href'
                    ),
                )
            )

        return forks

    @property
    def forkable(self):
        """True if the node's fork button is active"""
        return not 'disabled' in self.driver.find_element_by_css_selector(
            'a.node-fork-btn'
        ).get_attribute('class')

    @property
    def num_forks(self):
        """The number of forks, as displayed in the icon's counter on the node's
        dashboard
        """
        return int(self.driver.find_element_by_css_selector(
                '#overview div.btn-group:nth-of-type(2) a:nth-of-type(2)'
            ).text)

    @property
    def logs(self):
        """ The node's list of log entries.

        :returns: [``Log``, ...]
        """
        return logs.parse_log(
            container=self.driver.find_element_by_id('main-log')
        )

    def fork(self, split_driver=False):
        """Create a fork of the node.

         If split_driver is True, then reset self.driver to the original URL
         and return a new object. Otherwise, return a ``ProjectPage`` or
         ``ComponentPage`` as appropriate.
        """
        if split_driver:
            page = self._clone()
        else:
            page = self

        # Get the body element, so we know then the page has unloaded
        #body = self.driver.find_element_by_css_selector('body')

        with WaitForPageReload(self.driver):
            # click the fork icon
            page.driver.find_element_by_css_selector(
                '#overview div.btn-group:nth-of-type(2) a:nth-of-type(2)'
            ).click()

        # Wait at least until the page has unloaded to continue.
        # TODO: I think this is where the 2-3 second delay is. Fix that.
        #WebDriverWait(self.driver, 1).until(EC.staleness_of('body'))

        return page

    @property
    def can_add_file(self):

        files_page = self.driver.find_element_by_link_text(
            'Files'
        ).get_attribute('href')

        if files_page != self.driver.current_url:
            _url = self.driver.current_url
            self.driver.get(files_page)
        else:
            _url = None

        upload_button_class = self.driver.find_element_by_css_selector(
            'span.fileinput-button'
        ).get_attribute('class')

        if _url:
            self.driver.get(_url)

        return False if 'disabled' in upload_button_class else True

    @property
    def can_delete_files(self):

        files_page = self.driver.find_element_by_link_text(
            'Files'
        ).get_attribute('href')

        if files_page != self.driver.current_url:
            _url = self.driver.current_url
            self.driver.get(files_page)
        else:
            _url = None

        delete_button_class = self.driver.find_elements_by_css_selector(
            '.fileDeleteForm button.btn-delete'
        )[0].get_attribute('class')

        if _url:
            self.driver.get(_url)

        return False if 'disabled' in delete_button_class else True

    def add_file(self, f):
        """Add a file to the node."""

        # Click "Files" in the node's subnav
        self.driver.find_element_by_css_selector(
            '#overview div.subnav'
        ).find_element_by_link_text(
            'Files'
        ).click()

        self.driver.execute_script('''
            $('input[type="file"]').offset({left : 50});
        ''')

        with WaitForFileUpload(self.driver, wait=5):
            # Find file input
            field = self.driver.find_element_by_css_selector('input[type=file]')

            # Enter file into input
            field.send_keys(f if isinstance(f, basestring) else f.path)

            # Upload files
            self.driver.find_element_by_css_selector(
                'div.fileupload-buttonbar BUTTON.btn.btn-primary.start'
            ).click()

        # refresh the page. Normally this wouldn't be necessary, but BlueImp
        # doesn't work well with Selenium.
        #self.driver.get(self.driver.current_url)

    def delete_file(self, f):
        """Delete a file from the node"""

        # Click "Files" in the node's subnav
        self.driver.find_element_by_css_selector(
            '#overview div.subnav'
        ).find_element_by_link_text(
            'Files'
        ).click()

        WebDriverWait(self.driver, 3).until(
             EC.visibility_of_element_located(
                 (By.CSS_SELECTOR, 'tbody.files')
             )
        )

        row = [
            x for x in
            self.driver.find_elements_by_css_selector(
                '#filesTable tbody.files tr'
            )
            if x.find_element_by_css_selector('td.name a').text == f
        ]

        # row[0].find_element_by_css_selector('button.btn-delete').click()
        self.driver.find_element_by_css_selector('button.btn-delete').click()
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.modal.in button.btn-primary')
            )
        )

        self.driver.find_element_by_css_selector(
            'div.modal.in button.btn-primary'
        ).click()

    @property
    def files(self):
        F = namedtuple(
            'File',
            ('name', 'date_modified', 'file_size', 'downloads', 'url')
        )

        # Click "Files" in the node's subnav
        self.driver.find_element_by_css_selector(
            '#overview div.subnav'
        ).find_element_by_link_text(
            'Files'
        ).click()

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#filesTable')
            )
        )

        return [F(
            name=r.find_element_by_css_selector(
                'td.name a'
            ).text,
            date_modified=dt.datetime.strptime(
                r.find_element_by_css_selector(
                    'td:nth-of-type(2)'
                ).text,
                '%Y/%m/%d %I:%M %p'
            ),
            file_size=r.find_element_by_css_selector(
                'td.size'
            ).text,
            url=r.find_element_by_css_selector(
                'td.name a'
            ).get_attribute('href'),
            downloads=r.find_element_by_css_selector(
                'td:nth-of-type(4)'
            ).text,
        ) for r in self.driver.find_elements_by_css_selector(
            '#filesTable tbody.files tr'
        )]

    def _clone(self):
        new_driver = self.driver.__class__()
        new_driver.get(config.osf_home)

        # copy cookies
        for c in self.driver.get_cookies():
            new_driver.add_cookie(c)

        # load the current page.
        new_driver.get(self.driver.current_url)

        # return a copy of this class, with the new driver.
        return self.__class__(driver=new_driver)


class NodeSettingsPage(NodePage):
    @property
    def api_keys(self):
        creds = self.driver.find_elements_by_css_selector(
            'div.api-credential'
        )[-1]

        return [
            ApiKey(
                label=x.find_element_by_css_selector('span.api-label').text,
                key=x.find_element_by_css_selector('span.api-key').text,
            ) for x in creds
        ]

    def add_api_key(self, description=None):
        self.driver.get('{}/settings/'.format(config.osf_home))

        form = self.driver.find_element_by_id('create_key')

        form.find_element_by_css_selector('input[name="label"]').send_keys(
            description or "Automatically generated key"
        )

        with WaitForPageReload(self.driver):
            form.find_element_by_css_selector('button[type="submit"]').click()

        cred = self.driver.find_elements_by_css_selector(
            'div.api-credential'
        )[-1]

        return ApiKey(
            label=cred.find_element_by_css_selector('span.api-label').text,
            key=cred.find_element_by_css_selector('span.api-key').text,
        )

    def delete(self):
        from pages import UserDashboardPage

        title = self.title

        self.driver.find_element_by_id('delete-node').click()

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.modal.in')
            )
        )

        self.driver.find_element_by_css_selector(
            'div.modal.in input.bootbox-input'
        ).send_keys(title)

        with WaitForPageReload(self.driver):

            self.driver.find_element_by_css_selector(
                'div.modal.in button.btn-primary'
            ).click()

        return UserDashboardPage(driver=self.driver)


class ProjectPage(NodePage):
    """A project page, including subprojects."""

    def __init__(self, *args, **kwargs):

        # Require that an "id" or "driver" kwarg be passed
        if not (
            kwargs.get('id') or
            kwargs.get('driver') or
            kwargs.get('url')
        ):
            raise TypeError("A `url, `id`, or `driver` must be provided.")

        # If an ID is provided, build the URL for the project
        # TODO: Shouldn't this be in ProjectPage?
        if 'id' in kwargs:
            kwargs['url'] = '{}/project/{}/'.format(
                config.osf_home,
                kwargs['id'],
            )
            del kwargs['id']

        super(ProjectPage, self).__init__(*args, **kwargs)

    def add_component(self, title, component_type=None):
        """Add a component to the project.

        :param title: The title of the new component. Must be unique amongst
            components of this project.
        :param component_type: The type of component to create. Default "Other"

        :returns ComponentPage:
        """

        # Click "Add Component" button
        self.driver.find_element_by_css_selector(
            'a.btn[href="#newComponent"]'
        ).click()

        # Wait for the modal to be visible
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                #(By.CSS_SELECTOR, 'div.modal.fade.in')
                (By.ID, 'newComponent')
            )
        )

        # fill the modal form and submit it
        modal = self.driver.find_element_by_id('newComponent')

        modal.find_element_by_name('title').send_keys(title)
        modal.find_element_by_name('category').send_keys(
            component_type or 'Other'
        )
        modal.find_element_by_css_selector('button[type="submit"]').click()

        WebDriverWait(self.driver, 3).until(
            EC.invisibility_of_element_located(
                (By.ID, 'newComponent'),
            )
        )

        # get the link from the list of components
        components = [x for x
                      in self.driver.find_elements_by_css_selector('#Nodes a')
                      if x.text == title]

        # make sure there's only one component by that name.
        # TODO: We should perform this check before adding a component, too.
        if len(components) > 1:
            raise ValueError(
                'Multiple components named "{}" found.'.format(title)
            )

        # navigate to the new component
        # TODO: Make this option, but default?

        with WaitForPageReload(self.driver):
            components[0].click()

        # return the correct subclass of ``NodePage``
        if component_type == 'Project':
            return ProjectPage(driver=self.driver)
        return ComponentPage(driver=self.driver)

    def add_registration(self, registration_type=None, meta=None):
        """Add a component to the project.

        :param registration_type:
        :param meta: An iterable containing metadata for the registration, in
            the order it appears in the registration's form.

        :returns ProjectRegistrationPage:
        """
        # Go to the registrations page
        self.driver.find_element_by_css_selector(
            'div.subnav'
        ).find_element_by_link_text(
            'Registrations'
        ).click()

        # Click "New Registration"
        with WaitForPageReload(self.driver):
            self.driver.find_element_by_css_selector(
                'div.page-header a.btn'
            ).click()

        # Select the registration type
        with WaitForPageReload(self.driver):
            self.driver.find_element_by_css_selector(
                '.container select'
            ).send_keys(registration_type + "\n")

        # Fill the registration template
        fields = self.driver.find_elements_by_css_selector(
            '#registration_template textarea, '
            '#registration_template select'
        )

        # make sure we have the right number of strings in meta
        if len(fields) != len(meta):
            raise ValueError(
                'Length of meta argument ({}) must equal the number of form'
                'fields in the registration template ({})'.format(
                    len(meta),
                    len(fields)
                )
            )

        # fill the form (arbitrary length)
        for field, value in zip(fields, meta):
            field.send_keys(value)

        # Enter "continue"
        self.driver.find_elements_by_css_selector(
            '.container form input'
        )[-1].send_keys('continue')

        with WaitForPageReload(self.driver):
            # click "Register"
            self.driver.find_element_by_css_selector(
                '#register-submit'
            ).click()

        return ProjectRegistrationPage(driver=self.driver)


class ComponentPage(NodePage):
    """A component page"""
    pass


class ProjectRegistrationPage(ProjectPage):
    """A registration of a project"""

    @property
    def registration_meta(self):
        """ The registration's meta information, parsed from the "Registration
        Supplement" page.

        :returns: ``tuple``
        """

        url = self.driver.find_elements_by_css_selector(
            '#contributors a'
        )[-1].get_attribute('href')

        _url = self.driver.current_url

        # go to the registration meta page
        self.driver.get(url)

        meta = []

        for field in self.driver.find_elements_by_css_selector(
            '#registration_template textarea, '
            '#registration_template select'
        ):
            meta.append(
                field.get_attribute('value') or field.text
            )

        self.driver.get(_url)

        return tuple(meta)

    @property
    def registration_template(self):
        """The name of the registration template used, parsed from the header.
        """
        return self.driver.find_element_by_css_selector(
            '#overview a[href*="register"]'
        ).text

    @property
    def source_link(self):
        """ The URL of the node for which this is a registration."""

        return self.driver.find_element_by_css_selector(
            'span.label-important a'
        ).get_attribute('href')


class FilePage(NodePage):

    @property
    def versions(self):
        log = self.driver.find_element_by_css_selector(
            '#file-version-history tbody'
        )

        L = namedtuple('Log', ('version', 'date_uploaded', 'downloads', 'url'))

        return [L(
            x.find_element_by_css_selector('td:nth-child(1)').text,
            dt.datetime.strptime(
                x.find_element_by_css_selector('td:nth-child(2)').text,
                '%Y/%m/%d %I:%M %p',
            ),
            int(x.find_element_by_css_selector('td:nth-child(3)').text),
            x.find_element_by_css_selector(
                'td:nth-child(4) a'
            ).get_attribute('href'),
        ) for x in log.find_elements_by_css_selector('tr')]
