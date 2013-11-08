from pages import FILES
from pages.helpers import create_user
from tests.fixtures import UserFixture, ProjectFixture, SubprojectFixture
from tests.components.fixtures import ComponentFixture, ComponentOfProjectFixture, ComponentOfSubprojectFixture


class PublicProjectFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicProjectFixture, cls).setUpClass()
        cls.page.public = True


class PublicSubprojectFixture(SubprojectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicSubprojectFixture, cls).setUpClass()
        cls.page.public = True


class PublicComponentOfProjectFixture(ComponentOfProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicComponentOfProjectFixture, cls).setUpClass()
        cls.page.public = True


class PublicComponentOfSubprojectFixture(ComponentOfSubprojectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicComponentOfSubprojectFixture, cls).setUpClass()
        cls.page.public = True


class SubprojectOfPublicProjectFixture(PublicProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(SubprojectOfPublicProjectFixture, cls).setUpClass()
        cls.page = cls.page.add_component(
            title='Test Subproject',
            component_type='Project',
        )


class PublicSubprojectOfPublicProjectFixture(SubprojectOfPublicProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(PublicSubprojectOfPublicProjectFixture, cls).setUpClass()
        cls.page.public = True


class ComponentOfPublicProjectFixture(ComponentFixture, PublicProjectFixture):
    pass


class ComponentOfPublicSubprojectFixture(ComponentFixture, PublicSubprojectFixture):
    pass


class ComponentOfPublicSubprojectOfPublicProjectFixture(ComponentFixture, PublicSubprojectOfPublicProjectFixture):
    pass


class FileFixture(object):
    @classmethod
    def setUpClass(cls):
        super(FileFixture, cls).setUpClass()

        cls.page.add_file([x for x in FILES if x.name == 'test.jpg'][0])
        cls.file_url = '{}{}'.format(cls.page.driver.current_url, 'test.jpg')
        cls.page.driver.get(cls.file_url)


class ForkAccessFixture(object):
    @classmethod
    def setUpClass(cls):
        super(ForkAccessFixture, cls).setUpClass()

        cls.old_id = cls.page.id

        #create public and private subprojects and components
        cls.page = cls.page.add_component(
            title='Public Subproject',
            component_type='Project',
        )
        cls.page.public = True
        cls.page = cls.page.node(cls.old_id)

        cls.page = cls.page.add_component(
            title='Public Component',
        )
        cls.page.public = True
        cls.page = cls.page.node(cls.old_id)

        cls.page.add_component(
            title='Private Subproject',
            component_type='Project',
        )
        cls.page = cls.page.node(cls.old_id)

        cls.page.add_component(
            title='Private Component'
        )
        cls.page = cls.page.node(cls.old_id)

        # log in as second user
        cls.page.log_out()
        cls.users.append(create_user())
        cls.log_in(cls.users[-1])

        # fork project
        cls.page = cls.page.node(cls.old_id)
        cls.page.fork()


class AddContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.page.add_contributor(cls.users[-1])
        cls.old_id = cls.page.id


class AddContributorChildrenFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddContributorChildrenFixture, cls).setUpClass()

        cls.old_id = cls.page.id

        # create subproject
        cls.page = cls.page.add_component(
            title='Test Subproject',
            component_type='Project',
        )
        cls.subproject_id = cls.page.id
        cls.page = cls.page.node(cls.old_id)

        # create component
        cls.page = cls.page.add_component(
            title='Test Component',
        )
        cls.component_id = cls.page.id
        cls.page = cls.page.node(cls.old_id)

        cls.users.append(create_user())
        cls.page.add_contributor(cls.users[-1], children=True)

        cls.page = cls.page.node(cls.old_id)


class AddContributorAccessFixture(AddContributorFixture):
    @classmethod
    def setUpClass(cls):
        super(AddContributorAccessFixture, cls).setUpClass()
        cls.page.log_out()
        cls.log_in(cls.users[-1])
        cls.page = cls.page.node(cls.old_id, cls.project_id)


class AddMultiContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddMultiContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())
        cls.page.add_multi_contributor(cls.users[1], cls.users[2])


class AddMultiContributorDeleteFixture(object):
    @classmethod
    def setUpClass(cls):
        super(AddMultiContributorDeleteFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())
        cls.page.add_multi_contributor_delete(cls.users[-2], cls.users[-1])


class RemoveContributorFixture(object):
    @classmethod
    def setUpClass(cls):
        super(RemoveContributorFixture, cls).setUpClass()

        cls.users.append(create_user())
        cls.users.append(create_user())

        cls.page.add_multi_contributor(cls.users[1], cls.users[2])

        cls.page.remove_contributor(cls.users[1])
        cls.old_id = cls.page.id


class RemoveContributorAccessFixture(RemoveContributorFixture):
    @classmethod
    def setUpClass(cls):
        super(RemoveContributorAccessFixture, cls).setUpClass()
        cls.page.log_out()
        cls.log_in(cls.users[1])


class NonContributorModifyFixture(object):
    @classmethod
    def setUpClass(cls):
        super(NonContributorModifyFixture, cls).setUpClass()

        old_id = cls.page.id
        cls.page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        cls.page.log_out()
        cls.users.append(create_user())
        cls.log_in(cls.users[-1])

        cls.page = cls.page.node(old_id)


class ProjectNoDescriptionFixture(UserFixture):

    @classmethod
    def setUpClass(cls):
        super(ProjectNoDescriptionFixture, cls).setUpClass()
        cls.page = cls.page.new_project(
            title='Test Project',
            description=None
        )
        cls.page.type = 'project'

class DeleteProjectFixture(ProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(DeleteProjectFixture, cls).setUpClass()
        cls.project_url = cls.page.driver.current_url
        cls.page = cls.page.settings.delete()


class DeleteProjectwithComponentFixture(ComponentOfProjectFixture):
    @classmethod
    def setUpClass(cls):
        super(DeleteProjectwithComponentFixture, cls).setUpClass()
        cls.component_url = cls.page.driver.current_url
        cls.project_url = cls.page.parent_project().driver.current_url
        cls.page = cls.page.settings.delete()


class DeleteProjectwithSubprojectFixture(SubprojectFixture):
    @classmethod
    def setUpClass(cls):
        super(DeleteProjectwithSubprojectFixture, cls).setUpClass()
        cls.subproject_title = cls.page.title
        cls.subproject_url = cls.page.driver.current_url
        cls.project_url = cls.page.parent_project().driver.current_url
        cls.page = cls.page.settings.delete()


class WatchFixture(object):
    @classmethod
    def setUpClass(cls):
        super(WatchFixture, cls).setUpClass()
        cls.node_logs = cls.page.logs
        cls.old_num_watchers = cls.page.num_watchers
        cls.page.watched = True


class UnwatchFixture(WatchFixture):
    @classmethod
    def setUpClass(cls):
        super(UnwatchFixture, cls).setUpClass()
        cls.old_num_watchers = cls.page.num_watchers
        cls.page.watched = False
