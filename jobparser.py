from parser import ParseListingPage, ParseItemPage


class JobParser(ParseListingPage):

    """parse job based websites"""

    def __init__(self, url_tpl, keyword, baseurl):
        """setup parser parser """
        searchurl = url_tpl % (keyword, 1)
        ParseListingPage(JobParser, self).__init__(searchurl, baseurl)
        self.url_tpl = url_tpl
        self.keyword = keyword
        self.LISTING = None

    def next_page(self):
        """go to next page
        :returns: @todo

        """
        self.current_page += 1
        return self.url_tpl % (self.keyword, self.current_page)


class JobItem(ParseItemPage):
    """get job details"""
    def __init__(self, url, baseurl, keyword):
        ParseItemPage(JobItem, self).__init__(url, baseurl)
        self.TITLE = 'h1.jobtitle'
        self.DESC = 'div.templatetext'
        self.NAME = '.state-message'
        self.keyword = keyword

    def get_extra(self, data):
        """get extra data

        :data: @todo
        :returns: @todo

        """
        data['url'] = self.url
        data['name'] = self.dom.cssselect(self.NAME)[0].text_content().strip('-')
        data['keyword'] = self.keyword
        data['job_id'] = self.url.split('?')[0].split('/').pop()


