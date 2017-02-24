import unittest
from seek import Seek, Job as SeekJob
import util

URLS = ['www.seek.com.au', 'www.gumtree.com.au']


class TestSeek(unittest.TestCase):

    """test seek.com listing, description and pagination"""

    def test_listing(self):
        """
        test listing pages
        """
        parser = Seek('references')
        self.assertEqual('https://www.seek.com.au/jobs?keywords=references',
                         parser.url)
        parser.dom = util.dom_from_file('data/seek/seek.html')
        parser.get_listing()
        self.assertEqual(parser.items[0].text_content(),
                         'Red Cell Reference Technician')
        self.assertEqual(parser.items[1].text_content(),
                         'Reference Librarian')

    def test_job_details(self):
        """test getting job details
        :returns: @todo

        """
        job = SeekJob('https://www.seek.com.au/job/32839070')
        job.dom = util.dom_from_file('data/seek/job1.html')
        data = job.parse_page()
        self.assertEqual(data['title'], 'Red Cell Reference Technician - Sydney')
        self.assertNotEqual(data['description'], '')


if __name__ == '__main__':
    unittest.main()
