"""
runner class
"""
from app import gumtree, seek, db
import logging


class Runner(object):
    """docstring for App"""
    def __init__(self, scraper, keyword):
        super(Runner, self).__init__()
        self.scraper = scraper
        self.keyword = keyword
        self.db_name = '%s.db' % scraper

    def run(self):
        """runs the application
        :returns: @todo

        """
        db.create_db('%s.db' % self.scraper)
        if self.scraper == 'gumtree':
            parser = gumtree.GumTree(self.keyword)
        elif self.scraper == 'seek':
            parser = seek.Seek(self.keyword)
        parser.parse_listing_pages(job_parser, self.on_page_done,
                                   keyword=self.keyword,
                                   scraper=self.scraper)

    def on_page_done(self, data, success, failed):
        """@todo: Docstring for on_page_done.

        :done: @todo
        :success: @todo
        :failed: @todo
        :returns: @todo

        """
        logging.info("Success [%s]/ Failed [%s]", success, failed)
        stored, not_stored = db.store_to_db(self.db_name, data)
        logging.info("Saved [%s]/ Failed [%s]", stored, not_stored)



def job_parser(url, argv):
    """returns job parser

    :url: @todo
    :returns: @todo

    """
    frommod = 'app.%s' % argv['scraper']
    mod = __import__(frommod, fromlist=['Job'])
    job = getattr(mod, 'Job')
    return job(url, argv['keyword'])
