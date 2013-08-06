import util
import base
import os


class FileHandlingTests(base.ProjectSmokeTest):

    def setUp(self):

        super(FileHandlingTests, self).setUp()

        # Test file names
        self.images = _generate_full_filepaths({
            'jpg': 'test.jpg',
            'png': 'test.png',
            'gif': 'test.gif',
        })

        self.text_files = _generate_full_filepaths({
            'txt': 'txtfile.txt',
            'html': 'htmlfile.html',
        })

        self.archive_files = _generate_full_filepaths({
            'tar': 'text_files.tar',
            'tar.gz': 'text_files.tar.gz',
            'zip': 'text_files.zip',
        })

        self.archive_file_contents = ('txtfile.txt','htmlfile.html')

    def _add_file(self, path):
        self.goto('files')

        self.driver.execute_script('''
            $('input[type="file"]').offset({left : 50});
        ''')

        # Find file input
        field = self.driver.find_element_by_css_selector('input[type=file]')

        # Enter file into input
        field.send_keys(path)

        # Upload files
        self.driver.find_element_by_css_selector(
            'div.fileupload-buttonbar button.start'
        ).click()

    def _file_exists_in_project(self, filename):
        self.goto('file', filename)

        return filename in self.get_element('div.page-header h1').text

    def test_add_file(self):
        f = self.images['jpg']

        self._add_file(f['path'])

        self.assertTrue(
            self._file_exists_in_project(f['filename'])
        )

    def test_embedded_image_previews(self):

        for key in self.images:
            self._add_file(self.images[key]['path'])
            self.goto('file', self.images[key]['filename'])

            # Get the src attribute of the image embedded
            src_filename = self.get_element(
                '#file-container img[src*="{filename}"]'.format(
                    filename=self.images[key]['filename']
                )
            ).get_attribute('src').split('/')[-1]

            self.assertEqual(
                src_filename,
                self.images[key]['filename']
            )

    def test_embedded_text_preview(self):
        for key in self.text_files:
            self._add_file(self.text_files[key]['path'])
            self.goto('file', self.text_files[key]['filename'])
            with open(self.text_files[key]['path']) as f:
                contents = f.read()

            self.assertEqual(
                self.get_element('#file-container pre').text.strip(),
                contents.strip(),
            )

    def test_embedded_archive_preview(self):
        for key in self.archive_files:
            self._add_file(self.archive_files[key]['path'])
            self.goto('file', self.archive_files[key]['filename'])

            self.assertEqual(
                set(
                    self.get_element(
                        '#file-container pre'
                    ).text.strip().split('\n')[1:]
                ),
                set(self.archive_file_contents)
            )

util.generate_tests(FileHandlingTests)


def _generate_full_filepaths(file_dict):
    # Make each filename a full path
    for f in file_dict:
        file_dict[f] = {
            'path': os.path.join(  # append filename to this directory
                os.path.dirname(os.path.abspath(__file__)),
                'upload_files',
                file_dict[f]),
            'filename': file_dict[f],
        }

    return file_dict


if __name__ == '__main__':
    import unittest
    unittest.main()