"""
base parser class
"""
import app.util as util
import time
import logging


class Parser(object):

    """parse wiggle website"""
    def __init__(self, baseurl):
        super(Parser, self).__init__()
        self.baseurl = baseurl
        self.session = None
        self.url = None
        self.items = None
        self.dom = None
        self.givethembreak = 3

    def _download(self, url):
        """download the listing page
        :returns: @todo

        """
        self.dom = util.get_dom(url, self.baseurl, self.session)


class ParseListingPage(Parser):
    """parse listing pages"""

    def __init__(self, url, baseurl):
        super(ParseListingPage, self).__init__(baseurl)
        self.page_url = url
        self.current_page = 1
        self.LISTING = None

    def parse_listing_pages(self, itemparser, on_page_done, **argv):
        """parse all pages
        :returns: @todo

        """
        breakafter = 0
        tries = 0
        while True:
            try:
                logging.info("parsing page - %s", self.current_page)
                data, success, failed = self.download()\
                                            .get_listing()\
                                            .parse_items(itemparser, argv)
                on_page_done(data, success, failed)
                breakafter += 1
                if breakafter >= 2:
                    break
            except Exception as e:
                logging.exception(e)
                tries += 1
                if tries > 3:
                    print("Failed to continue: %s", e)
                    break

    def download(self):
        """download listing page
        :returns: @todo

        """
        self._download(self.next_page())
        return self

    def parse_items(self, itemparser, argv):
        """items to parse
        :returns: @todo

        """
        data = []
        success = 0
        failed = 0
        urls = 0
        for item in self.items:
            logging.info("parsing item: %s", item.text_content().strip())
            parser = itemparser(item.attrib['href'], argv)
            parser.session = self.session
            try:
                page_data = parser.download().parse_page()
                data.append(page_data)
            except IndexError:
                failed += 1
                continue
            success += 1
            urls += 1
            if urls >= 10:
                logging.info("sleeping")
                time.sleep(self.givethembreak)
                urls = 0
        return data, success, failed

    def get_listing(self):
        """return listings
        :returns: @todo

        """
        self.items = self.dom.cssselect(self.LISTING)
        return self

    def next_page(self):
        """load next page

        :f: @todo
        :returns: @todo

        """
        self.current_page += 1
        return self.page_url % self.current_page


class ParseItemPage(Parser):
    """parse details page"""
    def __init__(self, url, baseurl):
        super(ParseItemPage, self).__init__(baseurl)
        self.url = url
        self.TITLE = None
        self.DESC = None

    def download(self):
        """download page
        :returns: @todo

        """
        self._download(self.url)
        return self

    def get_title(self):
        """get product title

        :returns: @todo
        """
        return self.dom.cssselect(self.TITLE)[0]\
                   .text_content()\
                   .strip()

    def get_description(self):
        """get page description
        :returns: @todo

        """
        return self.dom.cssselect(self.DESC)[0].text_content().strip()

    def get_extra(self, data):
        """fills up other data, does nothing
        in parent class, should be extended in
        subclass

        :data: @todo
        :returns: @todo

        """
        pass

    def parse_page(self):
        """parsed the page for product data

        :returns: @todo
        """
        data = {}
        data['title'] = self.get_title()
        data['description'] = self.get_description()
        self.get_extra(data)
        return data
