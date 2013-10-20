from tests.fixtures import (
    ProjectFixture,
    SubprojectFixture,
    ComplexProjectFixture,
    ComplexSubprojectFixture,
)


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
            'wiki_content': cls.page.get_wiki_content(),
        }
        cls.page = cls.page.fork()


class ForkedProjectFixture(ForkFixture, ProjectFixture):
    pass


class ForkedSubprojectFixture(ForkFixture, SubprojectFixture):
    pass


class ForkedComplexProjectFixture(ForkFixture, ComplexProjectFixture):
    pass


class ForkedComplexSubprojectFixture(ForkFixture, ComplexSubprojectFixture):
    pass


class DeletedForkFixture(ForkFixture):

    @classmethod
    def setUpClass(cls):
        super(DeletedForkFixture, cls).setUpClass()
        cls.page.settings.delete()
        cls.page.driver.get(cls.parent_values['url'])


class DeletedProjectForkFixture(DeletedForkFixture, ProjectFixture):
    pass
