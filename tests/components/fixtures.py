from tests.fixtures import ProjectFixture, SubprojectFixture


class ComponentFixture(object):

    @classmethod
    def setUpClass(cls):
        super(ComponentFixture, cls).setUpClass()
        cls.parent_values = {
            'title': cls.page.title,
            'url': cls.page.driver.current_url,
        }

        cls.page = cls.page.add_component(
            title='Test Component',
            component_type='Other',
        )


class ComponentOfProjectFixture(ComponentFixture, ProjectFixture):
    pass


class ComponentOfSubprojectFixture(ComponentFixture, SubprojectFixture):
    pass


