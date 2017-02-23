from parser import ParseListingPage, ParseItemPage


class JobParser(ParseListingPage):

    """parse job based websites"""

    def __init__(self, url_tpl, keyword, baseurl):
        """setup parser parser """
        searchurl = url_tpl % (keyword, 1)
        super(JobParser, self).__init__(searchurl, baseurl)
        self.current_page = 1
        self.url_tpl = url_tpl
        self.keyword = keyword
        self.LISTING = None
        self.db_name = None

    def next_page(self):
        """go to next page
        :returns: @todo

        """
        self.current_page += 1
        return self.url_tpl % (self.keyword, self.current_page)


class JobItem(ParseItemPage):
    """get job details"""
    def __init__(self, url, baseurl, keyword):
        super(JobItem, self).__init__(url, baseurl)
        self.TITLE = None
        self.DESC = None
        self.NAME = None
        self.keyword = keyword

    def get_name(self):
        """implement in subclass
        :returns: @todo

        """
        raise NotImplementedError()

    def get_job_id(self):
        """implement in subclass
        :returns: @todo

        """
        raise NotImplementedError()

    def get_extra(self, data):
        """get extra data

        :data: @todo
        :returns: @todo

        """
        data['url'] = self.url
        data['keyword'] = self.keyword
        data['name'] = self.get_name()
        data['job_id'] = self.get_job_id()

