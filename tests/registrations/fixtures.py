from tests.fixtures import ProjectFixture, SubprojectFixture


#TODO: This should be a decorator.
def make_RegistrationTestCase(base_class):

    class RegistrationTestCase(base_class):

        registration_template = 'Open-Ended Registration'
        registration_meta = ('sample narrative', )

        @classmethod
        def setUpClass(cls):
            super(RegistrationTestCase, cls).setUpClass()

            cls.parent_values = {
                'title': cls.page.title,
                'component_names': cls.page.component_names,
                'contributors': cls.page.contributors,
                'date_created': cls.page.date_created,
                'last_updated': cls.page.last_updated,
                'logs': cls.page.logs,

            }

            cls.page = cls.page.add_registration(
                registration_type=cls.registration_template,
                meta=cls.registration_meta,
            )

    return RegistrationTestCase


class ProjectRegistrationTestCase(make_RegistrationTestCase(ProjectFixture)):
    pass


class SubprojectRegistrationTestCase(make_RegistrationTestCase(SubprojectFixture)):
    pass