"""
parses seek job
"""
import sys
from jobparser import JobParser, JobItem
import db
import logging

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
    def __init__(self, url):
        super(Job, self).__init__(url, BASEURL, sys.argv[1])
        self.TITLE = 'h1.jobtitle'
        self.DESC = 'div.templatetext'
        self.NAME = '.state-message'

    def get_name(self):
        """returns name
        :returns: @todo

        """
        return self.dom.cssselect(self.NAME)[0].text_content().strip('-')

    def get_job_id(self):
        """gets job id
        :returns: @todo

        """
        return self.url.split('?')[0].split('/').pop()


def on_page_done(data, success, failed):
    """@todo: Docstring for on_page_done.

    :done: @todo
    :success: @todo
    :failed: @todo
    :returns: @todo

    """
    logging.info("Success [%s]/ Failed [%s]", success, failed)
    db.store_to_db(DB_NAME, data)


def job_parser(url):
    """returns job parser

    :url: @todo
    :returns: @todo

    """
    return Job(url)


def main():
    """
    Entry point
    """
    logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
    db.create_db(DB_NAME)
    keyword = sys.argv[1]
    logging.info("Keyword: %s", keyword)
    seek = Seek(keyword)
    seek.parse_listing_pages(job_parser, on_page_done)

if __name__ == '__main__':
    main()
