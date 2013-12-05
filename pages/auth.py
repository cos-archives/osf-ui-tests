import config
import logs
from generic import ApiKey, OsfPage
from helpers import WaitForPageReload, Project, WebDriverWait
from static import HomePage
from project import ProjectPage
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class LoginPage(OsfPage):
    default_url = '{}/account/'.format(config.osf_home)
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

    def log_in_check(self, email, password):
        with WaitForPageReload(self.driver):
            form = self.driver.find_element_by_name('signin')
            form.find_element_by_id('username').send_keys(email)
            form.find_element_by_id('password').send_keys(password)
            form.find_element_by_css_selector('button[type=submit]').click()
        
        return LoginPage(driver=self.driver)

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
                'NAV.navbar.navbar-default UL.nav.navbar-nav li a[href="/dashboard/"]')
        ) == 1 else False

    def new_project(self, title, description=None):
        # Click "New Project"
        with WaitForPageReload(self.driver):
            self.driver.find_element_by_css_selector(
                'a[href="/project/new"]'
            ).click()

        # Fill the form
        self.driver.find_element_by_id('title').send_keys(title)
        if description:
            self.driver.find_element_by_id('description').send_keys(description)

        # Click "Create New Project"
        with WaitForPageReload(self.driver):
            self.driver.find_element_by_css_selector(
                'form[name="newProject"] button[type="submit"]'
            ).click()

        return ProjectPage(driver=self.driver)
    
    def get_alert_boxes(self, alert_text):
        WebDriverWait(self.driver, 3).until(
            ec.visibility_of_element_located(
                (
                 By.CSS_SELECTOR,
                 'div.alert.alert-block.alert-warning.fade.in'
                )
            )
        )
        alerts = self.driver.find_elements_by_xpath(
            '//*[text()[contains(translate(., "%s", "%s"), "%s")]]' %
            (alert_text.upper(), alert_text.lower(), alert_text.lower())
        )
        
        # Return matching alert boxes
        return alerts
 
    @property
    def profile_link(self):
        return self.driver.find_element_by_link_text(
            'My Public Profile'
        ).get_attribute('href')

    @property
    def profile(self):
        self.driver.get(self.profile_link)
        return UserProfilePage(driver=self.driver)

    @property
    def settings(self):
        self.driver.get('{}/settings'.format(config.osf_home))
        return UserSettingsPage(driver=self.driver)

    @property
    def projects(self):
        ul = self.driver.find_element_by_css_selector(
            'div.row div.col-md-6 ul.list-group'
        )

        p = []

        for li in ul.find_elements_by_css_selector('li.project'):
            link = li.find_element_by_css_selector('h4 span.overflow a')
            p.append(Project(
                title=link.text,
                url=link.get_attribute('href')
            ))

        return p

    @property
    def watch_logs(self):
        return logs.parse_log(
            container=self.driver.find_element_by_css_selector(
                'div.col-md-6:last-child'
            )
        )

class UserProfilePage(OsfPage):
    @property
    def full_name(self):
        return self.driver.find_element_by_id('profile-fullname').text

    @full_name.setter
    def full_name(self, value):
        self.driver.find_element_by_id('profile-fullname').click()

        field = self.driver.find_element_by_css_selector(
            'DIV.page-header DIV.editable-input INPUT.form-control.input-sm'
        )

        field.clear()
        field.send_keys(value)

        self.driver.find_element_by_css_selector(
            'DIV.page-header DIV.editable-buttons BUTTON.btn.btn-primary.btn-sm.editable-submit'
        ).click()

    @property
    def profile_shortlink(self):
        return self.driver.find_element_by_css_selector(
            '.container table a'
        ).get_attribute('href')


class UserSettingsPage(OsfPage):

    def __init__(self, *args, **kwargs):
        super(UserSettingsPage, self).__init__(*args, **kwargs)
        self.driver = kwargs.get('driver')

    def _verify_page(self):
        return self.driver.current_url[-10:] == '/settings/'

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
        self.driver.get('{}/settings'.format(config.osf_home))

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
