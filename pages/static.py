from generic import OsfPage

class HomePage(OsfPage):
    default_url = 'http://localhost:5000/'
    page_name = 'home page'

    def _verify_page(self):
        return True