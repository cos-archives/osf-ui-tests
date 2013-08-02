"""
Tests for file upload, download, and deletion.
"""

import os
import glob
import time
import unittest

# LXML imports
from lxml import etree
from lxml.html.diff import htmldiff

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Project imports
import base
import util
import config

# Get files for upload tests
file_dir = 'upload_files'
abs_files = [
    os.path.abspath(file)
    for file in glob.glob('%s/*' % file_dir)
]

# 
missing_file = 'this_file_is_missing'

def compare_html(html1, html2):
    """Compare two HTML files using lxml's htmldiff.

    Args:
        html1 : HTML file
        html2 : HTML file
    Returns:
        (bool) are the files different?

    """
    # Diff HTML files
    diff = htmldiff(html1, html2)

    # Wrap diff output in <diff> tags so lxml can parse
    diff = '<diff>%s</diff>' % (diff)

    # Parse diff
    elm = etree.fromstring(diff)

    # Find insert / delete notes
    ins_nodes = elm.xpath('//ins')
    del_nodes = elm.xpath('//del')

    # Check whether there are any nodes
    return len(ins_nodes) or len(del_nodes)

class FileTests(base.ProjectSmokeTest):
    
    def _add_files(self, files):
        """

        """
        # Browse to files page
        util.goto_files(self.driver)
        
        # Send file path to input
        for file in files:

            # Hack: Set input offset to positive value
            # Otherwise Selenium can't view the input
            self.driver.execute_script('''
                $('input[type="file"]').offset({left : 50});
            ''')

            # Find file input
            input = self.driver.find_element_by_xpath('//input[@type="file"]')
            
            # Enter file into input
            input.send_keys(file)

        # Upload files
        self.driver.find_element_by_css_selector(
            'div.fileupload-buttonbar button.start'
        ).click()
    
    def _get_file_link(self, file):
        """
        
        Args:
            ...
        Returns:
            (short file name, file link element)
        """
        # Strip path
        short_file = os.path.split(file)[-1]

        try:
            file_link = self.driver.find_element_by_xpath(
                '//a[@title="%s"]' % (short_file)
            )
        except NoSuchElementException:
            file_link = None

        return short_file, file_link
    
    def _get_tr(self, file_link):
        """
        """
        return file_link.find_element_by_xpath(
            'ancestor::tr'
        )

    @unittest.skip
    def test_add_files(self):
        """ Add several files. """
        
        # Add files
        self._add_files(abs_files)
            
        # Verify that files appear in files table
        for file in abs_files:
            _, file_link = self._get_file_link(file)
            self.assertTrue(file_link is not None)

    def _delete_file(self, file):
        #FIXME: file_link is apparently returning None.

        # Get file link
        _, file_link = self._get_file_link(file)

        # Click delete button
        file_link.find_element_by_xpath(
            'ancestor::tr//*[contains(@class, "btn-delete")]'
        ).click()

        return file_link

    @unittest.skip
    def test_delete_files(self):
        """ Add and delete several files. """

        # Add files
        self._add_files(abs_files)

        # Delete files
        for file in abs_files:

            # Delete the file
            file_link = self._delete_file(file)

            # Check whether file has been deleted. Table rows
            # for deleted files are hidden, not deleted, so we need
            # to check the element's is_displayed() method. It takes
            # a few seconds for the hide animation to complete, so
            # check repeatedly for a few seconds until the element
            # is hidden.
            deleted = False
            for tryidx in range(25):
                if not file_link.is_displayed():
                    deleted = True
                    break
                time.sleep(0.1)
            self.assertTrue(deleted)

    def _goto_file(self, file):
        """ Browse to a file within the current project. """
        
        # Build file URL
        file_url = os.path.join(self.project_url, 'files', file)
        
        # Browse to file
        self.driver.get(file_url)

    @unittest.skip('File not found not implemented yet.')
    def test_access_missing_file(self):
        """Try to access a missing file. Right now, this generates
        a 500 error from the server. Once the server generates a more
        informative error message, this test will need to be
        rewritten.

        """
        # Browse to file
        self._goto_file(missing_file)

        # Assert that file is not found
        pass
    
    @unittest.skip('File not found not implemented yet.')
    def test_access_deleted_file(self):
        
        # Add files
        self._add_files(abs_files)
        
        # Delete files
        for file in abs_files:

            self._delete_file(file)
        
        # Check that files can't be accessed
        for file in abs_files:

            # Browse to file
            self._goto_file(missing_file)

            # Assert that file is not found
            pass

            # Return to files page
            util.goto_files(self.driver)

    def _download_file(self, file):
        """
        
        """
        short_name, file_link = self._get_file_link(file)

        tr = self._get_tr(file_link)

        download_link = tr.find_element_by_xpath(
            '//a[@download="%s"]' % (short_name)
        )
        
        # Browse to download URL. We do this instead of clicking
        # on the link directly because some browsers (e.g. Chrome
        # trigger a file download when clicking on the link.
        self.driver.get(download_link.get_attribute('href'))
    
    @unittest.skip
    def test_file_version(self):
        #FIXME
        raise NotImplementedError()
        
        file = abs_files[0]

        for idx in range(5):

            self._add_files([file])

            # Get file link
            short_name, file_link = self._get_file_link(file)
            
            # Click on file link
            file_link.click()

            trs = self.driver.find_elements_by_tag_name('tr')

            # Assert that the number of <tr> elements equals the
            # loop index plus two (accounting for the header row
            # and the fact that the loop index is zero-based)
            self.assertEqual(len(trs), idx + 2)

    @unittest.skip
    def test_download_count(self):
        
        file = abs_files[0]

        self._add_files([file])

        for idx in range(5):
            
            # Download the file
            self._download_file(file)

            # Return to files page
            util.goto_files(self.driver)
     
            # Get file link
            short_name, file_link = self._get_file_link(file)
            
            # Click on file link
            file_link.click()

            trs = self.driver.find_elements_by_tag_name('tr')
            tds = trs[1].find_elements_by_tag_name('td')
            self.assertEqual(tds[2].text.strip(), str(idx + 1))

            # Return to files page
            util.goto_files(self.driver)
     
    @unittest.skip
    def test_download_files(self):
        #FIXME
        raise NotImplementedError()

        
        html_files = [file for file in abs_files if file.endswith('.html')]

        # Add files
        self._add_files(html_files)

        for file in html_files:
            
            # Download the file
            self._download_file(file)
            
            # Assert that the downloaded file is the same as
            # the file contents
            self.assertFalse(
                compare_html(
                    self.driver.page_source,
                    open(file).read()
                )
            )

            # Return to files page
            util.goto_files(self.driver)
     
    @unittest.skip
    def test_access_files(self):
        
        # Add files
        self._add_files(abs_files)

        for file in abs_files:
            
            # Get file link
            short_name, file_link = self._get_file_link(file)
            
            # Click on file link
            file_link.click()

            try:
                file_header = self.driver.find_element_by_xpath(
                    '//h1[contains(., "%s")]' % short_name
                )
            except NoSuchElementException:
                file_header = None

            self.assertTrue(file_header is not None)
            
            # Return to files page
            util.goto_files(self.driver)
     
# Generate tests
util.generate_tests(FileTests)

# Run tests
if __name__ == '__main__':
    unittest.main()
