"""
parses gumtree jobs
"""
from app.jobparser import JobParser, JobItem
import parsedatetime
import re

DB_NAME = 'gumtree.db'
BASEURL = 'https://www.gumtree.com.au/'
URL = 'http://www.gumtree.com.au/s-jobs/%s/page-%s/k0c9302?ad=offering'


class GumTree(JobParser):

    """parse gumtree.com"""

    def __init__(self, keyword):
        """setup GumTree parser """
        super(GumTree, self).__init__(URL, keyword, BASEURL)
        self.LISTING = '//a[@class="ad-listing__title-link"]'
        cal = parsedatetime.Calendar()
        self.TWENTY_FOUR_HR_OLD = cal.parse("24 hours ago")

    def should_exit(self):
        """check if older than 24 entry exists
        :returns: @todo

        """
        last_one = self.dom.xpath('//div[@class="ad-listing__date"]').pop()
        cal = parsedatetime.Calendar()
        post_time = cal.parse(last_one.text_content())
        return post_time < self.TWENTY_FOUR_HR_OLD

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
        self.TITLE = '//h1[@id="ad-title"]'
        self.DESC = '//div[@id="ad-description-details"]'
        self.NAME = '//div[@class="seller-profile__seller-detail"]//a'

    def get_name(self):
        """get name
        :returns: @todo

        """
        return self.dom.xpath(self.NAME)[0].text_content().strip()

    def get_job_id(self):
        """return job id
        :returns: @todo

        """
        return self.url.split('/').pop()
