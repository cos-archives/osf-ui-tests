from collections import namedtuple
import datetime as dt
import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as exc

from generic import OsfPage


class NodePage(OsfPage):

    def __init__(self, *args, **kwargs):
        if kwargs.get('id') is None and kwargs.get('driver') is None:
            raise TypeError("A `project_id` or `driver` must be provided.")

        if 'id' in kwargs:
            kwargs['url'] = 'http://localhost:5000/project/{}/'.format(
                kwargs['id']
            )
            del kwargs['id']

        super(NodePage, self).__init__(*args, **kwargs)

    def _verify_page(self):
        return len(self.driver.find_elements_by_id('node-title-editable')) == 1

    @property
    def date_created(self):
        date_string = self.driver.find_element_by_css_selector(
            '#contributors span.date:nth-of-type(1)').text

        return dt.datetime.strptime(date_string, '%Y/%m/%d %I:%M %p')

    @property
    def id(self):
        return urlparse.urlparse(
            self.driver.current_url
        ).path.strip('/').split('/')[-1]


    @property
    def title(self):
        return self._title.text

    @property
    def parent_title(self):
        try:
            return self.driver.find_element_by_css_selector(
                '#node-title a'
            ).text
        except exc.NoSuchElementException:
            return None


    @property
    def parent_link(self):
        return self.driver.find_element_by_css_selector(
            '#node-title a'
        ).get_attribute('href')

    @property
    def _title(self):
        return self.driver.find_element_by_id('node-title-editable')

    @property
    def components(self):
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
        return tuple([x.title for x in self.components])

    def parent_project(self):
        if self.parent_link:
            self.driver.get(self.parent_link)
            return ProjectPage(driver=self.driver)
        else:
            raise AttributeError("No parent project found.")


class ProjectPage(NodePage):
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

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.modal.fade.in')
            )
        )

        modal = self.driver.find_element_by_id('newComponent')

        # fill form
        modal.find_element_by_name('title').send_keys(title)
        modal.find_element_by_name('category').send_keys(
            component_type or 'Other'
        )
        modal.find_element_by_css_selector('button[type="submit"]').click()

        # get the link from the list of components
        components = [x for x
                      in self.driver.find_elements_by_css_selector('#Nodes a')
                      if x.text == title]

        if len(components) > 1:
            raise ValueError(
                'Multiple components named "{}" found.'.format(title)
            )

        components[0].click()

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

        if len(fields) != len(meta):
            raise ValueError(
                'Length of meta argument ({}) must equal the number of form'
                'fields in the registration template ({})'.format(
                    len(meta),
                    len(fields)
                )
            )

        for field, value in zip(fields, meta):
            field.send_keys(value)

        # Enter "continue"
        self.driver.find_elements_by_css_selector(
            '.container form input'
        )[-1].send_keys('continue')

        # click "Register"
        body = self.driver.find_element_by_css_selector('body')

        self.driver.find_element_by_css_selector(
            '.container form button'
        ).click()

        WebDriverWait(self.driver, 1).until(EC.staleness_of(body))

        return ProjectRegistrationPage(driver=self.driver)




class ComponentPage(NodePage):
    pass


class ProjectRegistrationPage(ProjectPage):
    @property
    def registration_meta(self):

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