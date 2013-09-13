import config
from generic import OsfPage


class HomePage(OsfPage):
    default_url = config.osf_home
    page_name = 'home page'

    def _verify_page(self):
        return True