import sys
from parser import ParseItemPage, ParseListingPage
import logging
import sqlite3


DB_NAME = 'seek.db'
BASEURL = 'https://www.seek.com.au/'
URL = 'https://www.seek.com.au/jobs?keywords=%s&page=%s'


class Seek(ParseListingPage):

    """parse seek.com"""

    def __init__(self, keyword):
        """setup seek parser """
        super(Seek, self).__init__(URL % (keyword, 1), BASEURL)
        self.keyword = keyword
        self.LISTING = 'article > h1 > a'

    def next_page(self):
        """go to next page
        :returns: @todo

        """
        self.current_page += 1
        return URL % (self.keyword, self.current_page)


class Job(ParseItemPage):
    """get job details"""
    def __init__(self, url):
        super(Job, self).__init__(url, BASEURL)
        self.TITLE = 'h1.jobtitle'
        self.DESC = 'div.templatetext'
        self.NAME = '.state-message'
        self.keyword = sys.argv[1]

    def get_extra(self, data):
        """get extra data

        :data: @todo
        :returns: @todo

        """
        data['url'] = self.url
        data['name'] = self.dom.cssselect(self.NAME)[0].text_content().strip('-')
        data['keyword'] = self.keyword
        data['job_id'] = self.url.split('?')[0].split('/').pop()


def job_parser(url):
    """returns job parser

    :url: @todo
    :returns: @todo

    """
    return Job(url)


def on_page_done(data, success, failed):
    """do something once we have downloaded a page

    :parser: the parser object
    :data: @todo
    :success: @todo
    :failed: @todo
    :returns: @todo

    """
    logging.info("Saving [%s]/ Failed [%s]", success, failed)
    build = []
    for job in data:
        build.append((job['url'], job['title'], job['description'],
                      job['name'], job['keyword'], job['job_id']))
    sql = """insert into jobs (url, title, description, name, keyword,
             job_id) values(?, ?, ?, ?, ?, ?)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executemany(sql, build)
    conn.commit()
    conn.close()


def create_db():
    """create database
    :returns: @todo

    """
    conn = sqlite3.connect(DB_NAME)
    sql = '''CREATE TABLE jobs (url text, title text, description text,
             name text, keyword text, job_id real unique)'''
    try:
        conn.execute(sql)
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()


def main():
    """
    Entry point
    """
    logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
    create_db()
    keyword = sys.argv[1]
    logging.info("Keyword: %s", keyword)
    seek = Seek(keyword)
    seek.parse_listing_pages(job_parser, on_page_done)

if __name__ == '__main__':
    main()
