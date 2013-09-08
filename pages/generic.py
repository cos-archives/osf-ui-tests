from selenium import webdriver

from pages.exceptions import PageException


class OsfPage(object):

    default_url = None

    def __init__(self, *args, **kwargs):
        # If no driver was passed, make a new default driver
        if kwargs.get('driver'):
            self.driver = kwargs.get('driver')
        else:
            self.driver = self._make_driver()

        if not kwargs.get('driver'):
            # If no driver was passed, go to the url passed or the default
            self.driver.get(kwargs.get('url', self.default_url))
        elif kwargs.get('url'):
            # If a driver was passed, go to the URL if provided.
            self.driver.get(kwargs.get('url'))

        # Verify the page is what you expect it to be.
        if not self._verify_page():
            raise PageException('Unexpected page structure: `{}`'.format(
                self.driver.current_url
            ))

    @property
    def logged_in(self):
        """ True if a user is logged in; else, False

         This is determined by examining the header bar, looking for a "log out"
         link
        """
        return len(
            self.driver.find_elements_by_css_selector(
                'ul#navbar-icons a[href="/logout"]'
            )
        ) > 0

    def log_out(self):
        self.driver.find_element_by_css_selector(
            'ul#navbar-icons a[href="/logout"]'
        ).click()

    def _make_driver(self):
        driver = webdriver.Firefox()
        driver.implicitly_wait(5)
        return driver

    def _verify_page(self):
        raise NotImplementedError('Page classes must define a `._verify_page()`'
                                  ' method')

    def close(self):
        self.driver.quit()