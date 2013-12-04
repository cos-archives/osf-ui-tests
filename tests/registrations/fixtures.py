from tests.fixtures import ComplexProjectFixture, ComplexSubprojectFixture


class RegistrationFixturetype1(object):

    registration_template = 'Open-Ended Registration'
    registration_meta = ('sample narrative', )

    @classmethod
    def setUpClass(cls):
        super(RegistrationFixturetype1, cls).setUpClass()

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


class ProjectRegistrationFixturetype1(RegistrationFixturetype1, ComplexProjectFixture):
    # The order here is important - fixtures' setUpClass() methods are called
    # right-to-left
    pass


class SubprojectRegistrationFixturetype1(
        RegistrationFixturetype1, ComplexSubprojectFixture):
    pass


class RegistrationFixturetype2(object):

    registration_template = 'OSF-Standard Pre-Data Collection Registration'
    registration_meta = ('No', 'No', 'sample narrative', )

    @classmethod
    def setUpClass(cls):
        super(RegistrationFixturetype2, cls).setUpClass()

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


class ProjectRegistrationFixturetype2(
    RegistrationFixturetype2,
    ComplexProjectFixture
):
    # The order here is important - fixtures' setUpClass() methods are called
    # right-to-left
    pass


class SubprojectRegistrationFixturetype2(
    RegistrationFixturetype2,
    ComplexSubprojectFixture
):
    pass


class RegistrationFixturetype3(object):
    registration_template = 'Replication Recipe (Brandt et al., 2013): Pre-Registration'
    registration_meta = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                         'no', 'j', 'k', 'l', 'm', 'n', 'o',
                         'Exact', 'Close', 'Different', 'Exact', 'Close', 'Different', 'Exact', 'p', 'q',
                         'r', 's', 't',)
    @classmethod
    def setUpClass(cls):
        super(RegistrationFixturetype3, cls).setUpClass()

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


class ProjectRegistrationFixturetype3(RegistrationFixturetype3, ComplexProjectFixture):
    # The order here is important - fixtures' setUpClass() methods are called
    # right-to-left
    pass


class SubprojectRegistrationFixturetype3(
        RegistrationFixturetype3, ComplexSubprojectFixture):
    pass


class RegistrationFixturetype4(object):
    registration_template = 'Replication Recipe (Brandt et al., 2013): Post-Completion'
    registration_meta = ('u',
                         'v', 'w', 'significantly different from the original effect size', 'inconclusive', 'x', 'y', 'z', '1',)
    @classmethod
    def setUpClass(cls):
        super(RegistrationFixturetype4, cls).setUpClass()

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


class ProjectRegistrationFixturetype4(RegistrationFixturetype4, ComplexProjectFixture):
    # The order here is important - fixtures' setUpClass() methods are called
    # right-to-left
    pass


class SubprojectRegistrationFixturetype4(
        RegistrationFixturetype4, ComplexSubprojectFixture):
    pass
