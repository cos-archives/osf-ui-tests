import util
import base
import os
import requests


class FileHandlingTests(base.ProjectSmokeTest):

    def setUp(self):

        super(FileHandlingTests, self).setUp()

        # Test file names
        self.files = {
            'jpg': 'test.jpg',
            'png': 'test.png',
            'gif': 'test.gif',
        }

        # Make each filename a full path
        for f in self.files:
            self.files[f] = {
                'path': os.path.join(  # append filename to this directory
                    os.path.dirname(os.path.abspath(__file__)),
                    'upload_files',
                    self.files[f]),
                'filename': self.files[f],
            }


    def _add_file(self, path):
        self.goto('files')

        self.driver.execute_script('''
            $('input[type="file"]').offset({left : 50});
        ''')

        # Find file input
        input = self.driver.find_element_by_css_selector('input[type=file]')

        # Enter file into input
        input.send_keys(path)

        # Upload files
        self.driver.find_element_by_css_selector(
            'div.fileupload-buttonbar button.start'
        ).click()

    def _file_exists_in_project(self, filename):
        self.goto('file', filename)

        return filename in self.get_element('div.page-header h1').text

    def test_add_file(self):
        f = self.files['jpg']

        self._add_file(f['path'])

        self.assertTrue(
            self._file_exists_in_project(f['filename'])
        )

    def test_embedded_image_previews(self):

        for key in self.files:
            self._add_file(self.files[key]['path'])
            self.goto('file', self.files[key]['filename'])

            src_filename = self.get_element(
                '#file-container img[src*="{filename}"]'.format(
                    filename=self.files[key]['filename']
                )
            ).get_attribute('src').split('/')[-1]

            self.assertEqual(
                src_filename,
                self.files[key]['filename']
            )

util.generate_tests(FileHandlingTests)

if __name__ == '__main__':
    import unittest
    unittest.main()