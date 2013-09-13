import config
from generic import OsfPage
from helpers import WaitForPageReload
from static import HomePage
from project import ProjectPage


class LoginPage(OsfPage):
    default_url = '{}/account'.format(config.osf_home)
    page_name = 'account management'

    def __init__(self, *args, **kwargs):

        super(LoginPage, self).__init__(*args, **kwargs)

    def _verify_page(self):
        return True if (
            'Create an Account' in self.driver.find_element_by_css_selector(
                'div.page-header h1').text
        ) else False

    @property
    def alerts(self):
        alerts = self.driver.find_elements_by_css_selector(
            'div#alert-container div.alert > p'
        )
        return [x.text for x in alerts]

    def log_in(self, user):
        with WaitForPageReload(self.driver):
            form = self.driver.find_element_by_name('signin')
            form.find_element_by_id('username').send_keys(user.email)
            form.find_element_by_id('password').send_keys(user.password)
            form.find_element_by_css_selector('button[type=submit]').click()

        return UserDashboardPage(driver=self.driver)

    def register(self, full_name, email, password, email2=None, password2=None):
        form = self.driver.find_element_by_name('registration')
        form.find_element_by_id('register-fullname').send_keys(full_name)
        form.find_element_by_id('register-username').send_keys(email)
        form.find_element_by_id('register-username2').send_keys(
            email if email2 is None else email2
        )
        form.find_element_by_id('register-password').send_keys(password)
        form.find_element_by_id('register-password2').send_keys(
            password if password2 is None else password2
        )
        form.find_element_by_css_selector('button[type=submit]').click()

        if 'account' in self.driver.current_url:
            return self
        else:
            return HomePage(driver=self.driver)


class UserDashboardPage(OsfPage):

    def __init__(self, *args, **kwargs):
        super(UserDashboardPage, self).__init__(*args, **kwargs)

        self.driver = kwargs.get('driver')

    def _verify_page(self):
        return True if len(
            self.driver.find_elements_by_css_selector(
                'div.navbar ul.nav li.active a[href="/dashboard"]')
        ) == 1 else False

    def new_project(self, title, description=None):
        # Click "New Project"
        self.driver.find_element_by_css_selector(
            'a[href="/project/new"]'
        ).click()

        # Fill the form
        self.driver.find_element_by_id('title').send_keys(title)
        if description:
            self.driver.find_element_by_id('description').send_keys(description)

        # Click "Create New Project"
        self.driver.find_element_by_css_selector(
            'form[name="newProject"] button[type="submit"]'
        ).click()

        return ProjectPage(driver=self.driver)