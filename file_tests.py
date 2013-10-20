import datetime as dt
import unittest
from unittest import skip

import base
import os
import requests
import tempfile
import time

from pages import FILES
from pages.helpers import get_new_project, WebDriverWait
from pages.project import FilePage
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


import urlparse

def prepend_api_url(url):

    parsed_url = urlparse.urlparse(url)
    prepended_url = parsed_url._replace(path='/api/v1' + parsed_url.path)
    return urlparse.urlunparse(prepended_url)

class FileTests(unittest.TestCase):

    def _subproject(self):
        """ Create and return a (sub)project which is the child of a project.

        The ``current_url`` of the driver is the subproject's overview.
        """
        return get_new_project().add_component(
            title='New Subproject',
            component_type='Project',
        )

    def _component(self):
        """ Create and return a (sub)project which is the child of a project.

        The ``current_url`` of the driver is the subproject's overview.
        """
        return get_new_project().add_component(
            title='New Component',
            component_type='Other',
        )

    def _subproject_component(self):
        """ Create and return a (sub)project which is the child of a project.

        The ``current_url`` of the driver is the subproject's overview.
        """
        return self._subproject().add_component(
            title='New Component',
            component_type='Other',
        )

    # Adding
    ########

    def _test_add_file(self, page):
        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        self.assertEqual(
            len(page.files),
            1
        )

        page.close()

    def test_project_add_file(self):
        self._test_add_file(get_new_project())

    def test_subproject_add_file(self):
        self._test_add_file(self._subproject())

    def test_component_add_file(self):
        self._test_add_file(self._component())

    @unittest.skip('known failure')
    def test_project_add_file_logged(self):
        # log says "component"; expected "project"

        page = get_new_project()
        _url = page.driver.current_url
        user = page.contributors[0]

        expected_log = (
            u'{user} added file {filename} to {node_type} {node_name}'.format(
                user=user.full_name,
                filename='test.jpg',
                node_type='project',
                node_name=page.title,
            )
        )

        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    def test_subproject_add_file_logged(self):

        page = self._subproject()
        _url = page.driver.current_url
        user = page.contributors[0]

        expected_log = (
            u'{user} added file {filename} to {node_type} {node_name}'.format(
                user=user.full_name,
                filename='test.jpg',
                node_type='project',
                node_name=page.title,
            )
        )

        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    @unittest.skip('known failure')
    def test_component_add_file_logged(self):
        # log says "project"; expected "component"

        page = self._component()
        _url = page.driver.current_url
        user = page.contributors[0]

        expected_log = (
            u'{user} added file {filename} to {node_type} {node_name}'.format(
                user=user.full_name,
                filename='test.jpg',
                node_type='component',
                node_name=page.title,
            )
        )

        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    @unittest.skip('known failure')
    def test_nested_component_add_file_logged(self):
        # log says "project"; expected "component"
        page = self._subproject_component()
        _url = page.driver.current_url
        user = page.contributors[0]

        expected_log = (
            u'{user} added file {filename} to {node_type} {node_name}'.format(
                user=user.full_name,
                filename='test.jpg',
                node_type='component',
                node_name=page.title,
            )
        )

        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            expected_log  # actual: 'component"
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        # Note: tests don't bubble up to this point
        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    # Deleting
    ##########

    def _test_delete_file(self, page):

        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        # make sure it's there - this triggers the necessary wait.
        self.assertIn(
            'test.jpg',
            [x.name for x in page.files]
        )

        page.delete_file('test.jpg')

        self.assertNotIn(
            'test.jpg',
            [x.name for x in page.files]
        )

        page.close()

    def test_project_delete_file(self):
        self._test_delete_file(get_new_project())

    def test_subproject_delete_file(self):
        self._test_delete_file(self._subproject())

    def test_component_delete_file(self):
        self._test_delete_file(self._component())

    @unittest.skip('known failure')
    def test_project_delete_file_logged(self):
        # log says "component"; expected "project"
        page = get_new_project()
        _url = page.driver.current_url
        user = page.contributors[0]
        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        # make sure it's there - this triggers the necessary wait.
        self.assertIn(
            'test.jpg',
            [x.name for x in page.files]
        )

        page.delete_file('test.jpg')

        expected_log = (
            u'{user} removed file {filename} '
            u'from {node_type} {node_name}'.format(
                user=user.full_name,
                filename='test.jpg',
                node_type='project',
                node_name=page.title,
            )
        )

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            expected_log  # actual: 'component"
        )

        page.close()

    def test_subproject_delete_file_logged(self):
        page = self._subproject()
        _url = page.driver.current_url
        user = page.contributors[0]
        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        # make sure it's there - this triggers the necessary wait.
        self.assertIn(
            'test.jpg',
            [x.name for x in page.files]
        )

        page.delete_file('test.jpg')

        expected_log = (
            u'{user} removed file {filename} '
            u'from {node_type} {node_name}'.format(
                user=user.full_name,
                filename='test.jpg',
                node_type='project',
                node_name=page.title,
            )
        )

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    @unittest.skip('known failure')
    def test_component_delete_file_logged(self):
        # log says "project"; expected "component"
        page = self._component()
        _url = page.driver.current_url
        user = page.contributors[0]
        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        # make sure it's there - this triggers the necessary wait.
        self.assertIn(
            'test.jpg',
            [x.name for x in page.files]
        )

        page.delete_file('test.jpg')

        expected_log = (
            u'{user} removed file {filename} '
            u'from {node_type} {node_name}'.format(
                user=user.full_name,
                filename='test.jpg',
                node_type='component',
                node_name=page.title,
            )
        )

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    @unittest.skip('known failure')
    def test_nested_component_delete_file_logged(self):
        # log says "project"; expected "component"
        page = self._subproject_component()

        _url = page.driver.current_url
        user = page.contributors[0]
        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])

        # make sure it's there - this triggers the necessary wait.
        self.assertIn(
            'test.jpg',
            [x.name for x in page.files]
        )

        page.delete_file('test.jpg')

        expected_log = (
            u'{user} removed file {filename} '
            u'from {node_type} {node_name}'.format(
                user=user.full_name,
                filename='test.jpg',
                node_type='component',
                node_name=page.title,
            )
        )

        page.driver.get(_url)

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    # Updating
    ##########

    def _test_file_update_logged(self, page):

        page_url = page.driver.current_url

        page.public = True

        fd, temp_file_path = tempfile.mkstemp(suffix='.txt', text=True)
        with open(temp_file_path, 'w') as tmp_file:
            tmp_file.write('first')

        # add the file to the project
        page.add_file(temp_file_path)

        with open(temp_file_path, 'w') as tmp_file:
            tmp_file.write('second')

        page.add_file(temp_file_path)

        # delete the temp file we made
        os.close(fd)
        os.remove(temp_file_path)

        page.driver.get(page_url)

        return page, os.path.basename(temp_file_path)

    @unittest.skip('expected failure')
    def test_project_file_update_logged(self):
        # log says "component", expected "project"
        page, filename = self._test_file_update_logged(get_new_project())
        user = page.contributors[0]

        expected_log = (
            u'{user} updated file {filename} in {node_type} {node_name}'.format(
                user=user.full_name,
                filename=filename,
                node_type='project',
                node_name=page.title,
            )
        )

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    def test_subproject_file_update_logged(self):
        page, filename = self._test_file_update_logged(self._subproject())
        user = page.contributors[0]

        expected_log = (
            u'{user} updated file {filename} in {node_type} {node_name}'.format(
                user=user.full_name,
                filename=filename,
                node_type='project',
                node_name=page.title,
            )
        )

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    @unittest.skip('expected failure')
    def test_nested_component_file_update_logged(self):
        # log says "project"; expected "component"
        page, filename = self._test_file_update_logged(
            self._subproject_component()
        )
        user = page.contributors[0]

        expected_log = (
            u'{user} updated file {filename} in {node_type} {node_name}'.format(
                user=user.full_name,
                filename=filename,
                node_type='component',
                node_name=page.title,
            )
        )

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    @unittest.skip('expected failure')
    def test_component_file_update_logged(self):
        # expected "component"; got "project"
        page, filename = self._test_file_update_logged(self._component())
        user = page.contributors[0]

        expected_log = (
            u'{user} updated file {filename} in {node_type} {node_name}'.format(
                user=user.full_name,
                filename=filename,
                node_type='component',
                node_name=page.title,
            )
        )

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page = page.parent_project()

        self.assertEqual(
            page.logs[0].text,
            expected_log
        )

        page.close()

    # Timestamped Filenames
    #######################

    def _test_file_extensions(self, page):

        page_url = page.driver.current_url

        page.public = True

        fd, temp_file_path = tempfile.mkstemp(suffix='.txt', text=True)
        with open(temp_file_path, 'w') as tmp_file:
            tmp_file.write('first')

        # add the file to the project
        page.add_file(temp_file_path)

        with open(temp_file_path, 'w') as tmp_file:
            tmp_file.write('second')

        page.add_file(temp_file_path)

        page.close()

        # delete the temp file we made
        os.close(fd)
        os.remove(temp_file_path)

        file_url = '{}files/download/{}/version/1/'.format(
            prepend_api_url(page_url),
            os.path.basename(temp_file_path),
        )

        f = requests.get(file_url, verify=False)

        filename = f.headers['content-disposition'].split('=')[-1]

        filename_date = dt.datetime.strptime(
            filename[:-4].split('_')[-1],
            '%Y%m%d%H%M%S'
        )

        self.assertAlmostEqual(
            filename_date,
            dt.datetime.utcnow(),
            delta=dt.timedelta(minutes=2)
        )

    def test_project_file_extensions(self):
        self._test_file_extensions(get_new_project())

    def test_subproject_file_extensions(self):
        self._test_file_extensions(self._subproject())

    def test_component_file_extensions(self):
        self._test_file_extensions(self._component())

    # Download Counter
    ##################

    def _test_file_download_count(self, page):

        page_url = page.driver.current_url

        page.public = True

        fd, temp_file_path = tempfile.mkstemp(suffix='.txt', text=True)
        with open(temp_file_path, 'w') as tmp_file:
            tmp_file.write('first')

        # add the file to the project
        page.add_file(temp_file_path)

        with open(temp_file_path, 'w') as tmp_file:
            tmp_file.write('second')

        page.add_file(temp_file_path)

        # delete the temp file we made
        os.close(fd)
        os.remove(temp_file_path)

        file_url = '{}files/{}'.format(
            page_url,
            os.path.basename(temp_file_path),
        )

        page = FilePage(driver=page.driver)
        page.driver.get(file_url)

        self.assertEqual(
            [x.downloads for x in page.versions],
            [0, 0]
        )

        file_url = '{}files/download/{}/version/1/'.format(
            prepend_api_url(page_url),
            os.path.basename(temp_file_path),
        )

        f = requests.get(file_url, verify=False)

        page.driver.get(page.driver.current_url)

        self.assertEqual(
            [x.downloads for x in page.versions],
            [0, 1]
        )

        page.close()

    def test_project_file_download_count(self):
        self._test_file_download_count(get_new_project())

    def test_subproject_file_download_count(self):
        self._test_file_download_count(self._subproject())

    def test_component_file_download_count(self):
        self._test_file_download_count(self._component())

    # File modification controls
    ############################

    def _test_file_controls_not_present(self, page, second_user=False):

        page.add_file([x for x in FILES if x.name == 'test.jpg'][0])
        files_url = page.driver.current_url

        page.public = True

        page.log_out()

        page.driver.get(files_url)

        WebDriverWait(page.driver, 3).until(
            ec.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#fileupload div.fileupload-buttonbar .disabled'
                )
            )
        )

        # all three buttons in the upload header should be disabled
        self.assertEqual(
            len(
                page.driver.find_elements_by_css_selector(
                    '#fileupload div.fileupload-buttonbar .disabled'
                )
            ),
            2
        )

        # the delete button for the file should also be disabled
        self.assertEqual(
            len(
                page.driver.find_elements_by_css_selector(
                    'form.fileDeleteForm button.btn-delete.disabled'
                )
            ),
            1
        )

        page.close()

    def test_project_file_controls_not_present_anonymous(self):
        self._test_file_controls_not_present(get_new_project())

    def test_subproject_file_controls_not_present_anonymous(self):
        self._test_file_controls_not_present(self._subproject())

    def test_component_file_controls_not_present_anonymous(self):
        self._test_file_controls_not_present(self._component())


class FileHandlingTests(base.ProjectSmokeTest):

    def setUp(self):

        super(FileHandlingTests, self).setUp()

    def _file_exists_in_project(self, filename):
        """Goes to a file's page, verifies by checking the title."""
        self.goto('file', filename)

        return filename in self.get_element('div.page-header h1').text

    def test_embedded_image_previews(self):
        """Test that image file pages include the image as an <img> element"""

        for key in self.image_files:
            self.add_file(self.image_files[key]['path'])
            self.goto('file', self.image_files[key]['filename'])

            # Get the src attribute of the image embedded
            src_filename = self.get_element(
                '#file-container img[src*="{filename}"]'.format(
                    filename=self.image_files[key]['filename']
                )
            ).get_attribute('src').strip('/').split('/')[-1]

            self.assertEqual(
                src_filename,
                self.image_files[key]['filename']
            )

    def test_embedded_text_preview(self):
        for key in self.text_files:
            self.add_file(self.text_files[key]['path'])
            self.goto('file', self.text_files[key]['filename'])

            # read the contents of the source file
            with open(self.text_files[key]['path']) as f:
                contents = f.read()

            # make sure they match the contents of the <pre> element.
            self.assertEqual(
                self.get_element('#file-container pre').text.strip(),
                contents.strip(),
            )

    def test_embedded_archive_preview(self):
        for key in self.archive_files:
            self.add_file(self.archive_files[key]['path'])
            self.goto('file', self.archive_files[key]['filename'])

            # Check that the file list in the <pre> element matches the
            # archive's content.
            self.assertEqual(
                set(
                    self.get_element(
                        '#file-container pre'
                    ).text.strip().split('\n')[1:]  # Exclude the first line.
                ),
                set(self.archive_file_contents)
            )

    def test_too_large_to_embed(self):
        """Make sure very large text files are not rendered in-browser"""

        # generate a 3MB temporary file
        fd, temp_file_path = tempfile.mkstemp(suffix='.txt', text=True)
        with open(temp_file_path, 'w') as tmp_file:
            for _ in xrange(100000):
                tmp_file.write('Hello, Open Science Framework!')

        # add the file to the project
        self.add_file(temp_file_path)
        self.goto('file', os.path.split(temp_file_path)[-1])

        # check that it is not rendered in the browser
        self.assertTrue(
            'file is too large' in self.get_element('div#file-container').text
        )

        # delete the temp file we made
        os.close(fd)
        os.remove(temp_file_path)

    def test_not_embeddable(self):
        """Upload a non-embedable file and make sure it's not embedded"""
        f = self.binary_files['pdf']

        self.add_file(f['path'])
        self.goto('file', f['filename'])

        self.assertTrue(
            'cannot be rendered' in self.get_element('div#file-container').text
        )

    def test_most_recent_version_displayed(self):
        f = self.add_versioned_file()

        # assert that string from version 1 is present in embed.
        self.goto('file', f)
        self.assertTrue(
            'Version 1' in self.get_element('#file-container pre').text.strip()
        )

    def test_version_history(self):
        f = self.add_versioned_file()

        self.goto('file', f)
        # topmost history entry is the current version
        self.assertTrue(
            'current' in self.get_element(
                '#file-version-history tbody tr:first-child td:first-child'
            ).text
        )
        # second topmost entry is revision 1.
        self.assertTrue(
            '1' in self.get_element(
                '#file-version-history tbody tr:nth-of-type(2) td:first-child'
            ).text
        )

        # make the project public so requests can access it w/o being logged in.
        self.goto('dashboard')
        self.make_public()

        self.goto('file', f)

        # see that the added text is in the current version
        self.assertIn(
            'Version 1',
            requests.get(
                self.get_element(
                    '#file-version-history tbody tr:first-child a'
                ).get_attribute('href'),
                verify=False
            ).content,
        )

        # ... but isn't in the first version.
        self.assertNotIn(
            'Version 1',
            requests.get(
                self.get_element(
                    '#file-version-history tbody tr:last-child a'
                ).get_attribute('href'),
                verify=False
            ).content,
        )


    @skip('Not Implemented')
    def test_access_file_not_found(self):
        raise NotImplementedError

    @skip('Not Implemented')
    def test_download_count(self):
        raise NotImplementedError