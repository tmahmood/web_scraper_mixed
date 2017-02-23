"""
parses gumtree jobs
"""
import sys
from jobparser import JobParser, JobItem
import logging
import db

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
    def __init__(self, url):
        super(Job, self).__init__(url, BASEURL, sys.argv[0])
        self.TITLE = 'h1#ad-title'
        self.DESC = 'div#ad-description-details'
        self.NAME = '.seller-profile__seller-detail a'

    def get_name(self):
        """get name
        :returns: @todo

        """
        return self.dom.cssselect(self.NAME)[0].text_content().strip(' - ')

    def get_job_id(self):
        """return job id
        :returns: @todo

        """
        return self.url.split('/').pop()


def job_parser(url):
    """returns job parser

    :url: @todo
    :returns: @todo

    """
    return Job(url)


def on_page_done(data, success, failed):
    """@todo: Docstring for on_page_done.

    :done: @todo
    :success: @todo
    :failed: @todo
    :returns: @todo

    """
    logging.info("Success [%s]/ Failed [%s]", success, failed)
    db.store_to_db(DB_NAME, data)


def main():
    """
    Entry point
    """
    logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
    db.create_db(DB_NAME)
    keyword = sys.argv[1]
    logging.info("Keyword: %s", keyword)
    gumtree = GumTree(keyword)
    gumtree.parse_listing_pages(job_parser, on_page_done)

if __name__ == '__main__':
    main()
