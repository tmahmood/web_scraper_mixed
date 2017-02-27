"""
parses seek job
"""
from app.jobparser import JobParser, JobItem
import re

DB_NAME = 'seek.db'
BASEURL = 'https://www.seek.com.au/'
URL = 'https://www.seek.com.au/jobs?keywords=%s&page=%s&daterange=1'


class Seek(JobParser):

    """parse seek.com"""

    def __init__(self, keyword):
        """setup seek parser """
        super(Seek, self).__init__(URL, keyword, BASEURL)
        self.LISTING = '//article//h1//a'

    def should_exit(self):
        """check if older than 24 entry exists
        :returns: @todo

        """
        anext = self.dom.xpath('//a[@data-automation="page-next"]')
        if len(anext) == 0:
            return True
        return False

    def match_criteria(self, page_data):
        """check if description contains email address

        :page_data: @todo
        :returns: @todo

        """
        return re.search(string=page_data['description'],
                  pattern=r'[\w*\.-]+@[\w*\.-]+') != None


class Job(JobItem):
    """get job details"""
    def __init__(self, url, keyword):
        super(Job, self).__init__(url, BASEURL, keyword)
        self.TITLE = '//h1[@class="jobtitle"]'
        self.DESC = '//div[@class="templatetext"]'
        self.NAME = '//span[@class="state-message"]'

    def get_name(self):
        """returns name
        :returns: @todo

        """
        return self.dom.xpath(self.NAME)[0].text_content().strip(' - ')

    def get_job_id(self):
        """gets job id
        :returns: @todo

        """
        return self.url.split('?')[0].split('/').pop()

    def failed_parsing(self, whichone):
        """check which one failed to parse
        and try to do something about it

        :whichone: @todo
        :returns: @todo

        """
        if whichone == "title":
            return self.dom.xpath('//h1').pop(0).text_content()
        if whichone == 'description':
            cls = '//div[@class="state-floatleft grid_6 state-job-ad"]'
            return self.dom.xpath(cls).pop(0).text_content()


