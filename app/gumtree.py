"""
parses gumtree jobs
"""
from app.jobparser import JobParser, JobItem

DB_NAME = 'gumtree.db'
BASEURL = 'https://www.gumtree.com.au/'
URL = 'https://www.gumtree.com.au/s-%s/page-%s/k0'


class GumTree(JobParser):

    """parse gumtree.com"""

    def __init__(self, keyword):
        """setup GumTree parser """
        super(GumTree, self).__init__(URL, keyword, BASEURL)
        self.LISTING = 'a.ad-listing__title-link'


class Job(JobItem):
    """get job details"""
    def __init__(self, url, keyword):
        super(Job, self).__init__(url, BASEURL, keyword)
        self.TITLE = 'h1#ad-title'
        self.DESC = 'div#ad-description-details'
        self.NAME = '.seller-profile__seller-detail a'

    def get_name(self):
        """get name
        :returns: @todo

        """
        return self.dom.cssselect(self.NAME)[0].text_content().strip()

    def get_job_id(self):
        """return job id
        :returns: @todo

        """
        return self.url.split('/').pop()
