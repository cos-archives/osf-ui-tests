from tests.fixtures import ProjectFixture, SubprojectFixture


class ForkFixture(object):

    @classmethod
    def setUpClass(cls):
        super(ForkFixture, cls).setUpClass()
        cls.parent_values = {
            'url': cls.page.driver.current_url,
            'title': cls.page.title,
            'components': cls.page.components,
            'date_created': cls.page.date_created,
            'logs': cls.page.logs,
        }
        cls.page = cls.page.fork()


class ForkedProjectFixture(ForkFixture, ProjectFixture):
    pass


class ForkedSubprojectFixture(ForkFixture, SubprojectFixture):
    pass