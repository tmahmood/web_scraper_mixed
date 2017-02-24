"""
parses seek job
"""
from app.jobparser import JobParser, JobItem

DB_NAME = 'seek.db'
BASEURL = 'https://www.seek.com.au/'
URL = 'https://www.seek.com.au/jobs?keywords=%s&page=%s'


class Seek(JobParser):

    """parse seek.com"""

    def __init__(self, keyword):
        """setup seek parser """
        super(Seek, self).__init__(URL, keyword, BASEURL)
        self.LISTING = 'article > h1 > a'


class Job(JobItem):
    """get job details"""
    def __init__(self, url, keyword):
        super(Job, self).__init__(url, BASEURL, keyword)
        self.TITLE = 'h1.jobtitle'
        self.DESC = 'div.templatetext'
        self.NAME = '.state-message'

    def get_name(self):
        """returns name
        :returns: @todo

        """
        return self.dom.cssselect(self.NAME)[0].text_content().strip(' - ')

    def get_job_id(self):
        """gets job id
        :returns: @todo

        """
        return self.url.split('?')[0].split('/').pop()
