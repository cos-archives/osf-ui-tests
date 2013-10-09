from tests.fixtures import UserFixture


class ProjectNoDescriptionFixture(UserFixture):

    @classmethod
    def setUpClass(cls):
        super(ProjectNoDescriptionFixture, cls).setUpClass()
        cls.page = cls.page.new_project(
            title='Test Project',
            description=None
        )