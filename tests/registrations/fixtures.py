from tests.fixtures import ComplexProjectFixture, ComplexSubprojectFixture


class RegistrationFixture(object):

    registration_template = 'Open-Ended Registration'
    registration_meta = ('sample narrative', )

    @classmethod
    def setUpClass(cls):
        super(RegistrationFixture, cls).setUpClass()

        cls.parent_values = {
            'title': cls.page.title,
            'component_names': cls.page.component_names,
            'contributors': cls.page.contributors,
            'date_created': cls.page.date_created,
            'last_updated': cls.page.last_updated,
            'logs': cls.page.logs,
            'url': cls.page.driver.current_url,

        }

        cls.page = cls.page.add_registration(
            registration_type=cls.registration_template,
            meta=cls.registration_meta,
        )


class ProjectRegistrationFixture(RegistrationFixture, ComplexProjectFixture):
    # The order here is important - fixtures' setUpClass() methods are called
    # right-to-left
    pass


class SubprojectRegistrationFixture(
        RegistrationFixture, ComplexSubprojectFixture):
    pass