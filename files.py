import util
import base
import os
import shutil
import tempfile


class FileHandlingTests(base.ProjectSmokeTest):

    def setUp(self):

        super(FileHandlingTests, self).setUp()

        # Test file names
        self.images = self._generate_full_filepaths({
            'jpg': 'test.jpg',
            'png': 'test.png',
            'gif': 'test.gif',
        })

        self.text_files = self._generate_full_filepaths({
            'txt': 'txtfile.txt',
            'html': 'htmlfile.html',
        })

        self.archive_files = self._generate_full_filepaths({
            'tar': 'text_files.tar',
            'tar.gz': 'text_files.tar.gz',
            'zip': 'text_files.zip',
        })
        self.archive_file_contents = ('txtfile.txt','htmlfile.html')

        self.binary_files = self._generate_full_filepaths({
            'pdf': 'pdffile.pdf',
        })

        self.versioned_files = self._generate_full_filepaths({
            0: 'versioned-0.txt',
            1: 'versioned-1.txt',
        })


    def test_add_file(self):
        """Add a file to a project, then make sure its page exists"""
        f = self.images['jpg']

        self._add_file(f['path'])

        self.assertTrue(
            self._file_exists_in_project(f['filename'])
        )

    def test_embedded_image_previews(self):
        """Test that image file pages include the image as an <img> element"""

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
            self._add_file(self.archive_files[key]['path'])
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
        self._add_file(temp_file_path)
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

        self._add_file(f['path'])
        self.goto('file', f['filename'])

        self.assertTrue(
            'cannot be rendered' in self.get_element('div#file-container').text
        )

    def test_most_recent_version_displayed(self):
        f = self._add_versioned_file(self.text_files, self.versioned_files)

        # assert that string from version 1 is present in embed.
        self.goto('file', f)
        self.assertTrue(
            'Version 1' in self.get_element('#file-container pre').text.strip()
        )

    def test_version_history(self):
        f = self._add_versioned_file(self.text_files, self.versioned_files)

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


    def test_delete_file(self):
        #add a file
        f = self.images['jpg']
        self._add_file(f['path'])

        #delete the added file
        self.goto('files')
        self.driver.find_element_by_css_selector('td form button').click()

        #check the file not exist
        self.goto('file', f['filename'])

        self.assertEqual(self.driver.find_element_by_css_selector("h1").text, u'Not Found')




util.generate_tests(FileHandlingTests)



if __name__ == '__main__':
    import unittest
    unittest.main()