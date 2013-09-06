import datetime as dt
import urlparse
from collections import namedtuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as exc

import logs
from generic import OsfPage


class NodePage(OsfPage):
    """Base class for Component and Project pages. In other words, anything that
    is represented as a ``Node`` model in the backend.

    It should not be instantiated directly.
    """

    def __init__(self, *args, **kwargs):

        # Require that an "id" or "driver" kwarg be passed
        if kwargs.get('id') is None and kwargs.get('driver') is None:
            raise TypeError("A `id` or `driver` must be provided.")

        # If an ID is provided, build the URL for the project
        # TODO: Shouldn't this be in ProjectPage?
        if 'id' in kwargs:
            kwargs['url'] = 'http://localhost:5000/project/{}/'.format(
                kwargs['id']
            )
            del kwargs['id']

        super(NodePage, self).__init__(*args, **kwargs)

    def _verify_page(self):
        """ Return True if the current page is the one expected for a
        ``NodePage``."""
        return len(self.driver.find_elements_by_id('node-title-editable')) == 1

    @property
    def contributors(self):
        """ A list of contributors for the node, parsed from the
        header.

        :returns: [``Contributor``, ...]
        """
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
    def date_created(self):
        """ The date the node was created, parsed from the header.

        :returns: ``datetime.datetime``
        """
        date_string = self.driver.find_element_by_css_selector(
            '#contributors span.date:nth-of-type(1)').text

        return dt.datetime.strptime(date_string, '%Y/%m/%d %I:%M %p')

    @property
    def last_updated(self):
        """ When the node was last updated, parsed from the header.

        :returns: ``datetime.datetime``
        """
        date_string = self.driver.find_element_by_css_selector(
            '#contributors span.date:nth-of-type(2)').text

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
    def title(self):
        """The node's title, parsed from the header

        :returns: ``str``
        """
        return self._title.text

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
            '#node-title a'
        ).get_attribute('href')

    @property
    def _title(self):
        """The node's title element.

        :returns: ``WebElement``
        """
        return self.driver.find_element_by_id('node-title-editable')

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

    def set_wiki_content(self, content, page='home'):
        """Sets the content of a wiki page.

        :param content: string to be set as the page's content.
        :param page: Optional. The wiki page to set. Defaults to "home"
        """
        _url = self.driver.current_url

        self.driver.get(
            '{}/wiki/{}/edit'.format(
                _url.strip('/'),
                page
            )
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

        # for each list entry
        for r in  self.driver.find_elements_by_css_selector(
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
                        r.text.split('registered: ')[-1],
                        '%Y/%m/%d %I:%M %p'
                    ),
                )
            )

        return registrations

    @property
    def logs(self):
        """ The node's list of log entries.

        :returns: [``Log``, ...]
        """
        return logs.parse_log(
            container=self.driver.find_element_by_id('main-log')
        )


class ProjectPage(NodePage):
    """A project page, including subprojects."""

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
                (By.CSS_SELECTOR, 'div.modal.fade.in')
            )
        )



        # fill the modal form and submit it
        modal = self.driver.find_element_by_id('newComponent')

        modal.find_element_by_name('title').send_keys(title)
        modal.find_element_by_name('category').send_keys(
            component_type or 'Other'
        )
        modal.find_element_by_css_selector('button[type="submit"]').click()

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
        self.driver.find_element_by_link_text('New Registration').click()

        # Select the registration type
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

        # Get the body element, so we know then the page has unloaded
        body = self.driver.find_element_by_css_selector('body')

        # click "Register"
        self.driver.find_element_by_css_selector(
            '.container form button'
        ).click()

        # Wait at least until the page has unloaded to continue.
        # TODO: I think this is where the 2-3 second delay is. Fix that.
        WebDriverWait(self.driver, 1).until(EC.staleness_of(body))

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