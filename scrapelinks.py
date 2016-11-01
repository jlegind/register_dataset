import requests
from bs4 import BeautifulSoup as bs
import re


class ScrapeLinks(object):
    """Processes a simple HTML page with DwC archive zip files and returns the individual links."""

    def __init__(self, url, baseurl):
        '''
        :param url: url to the webpage. Must be directly accessible.
        :param baseurl: May be needed to concatenate with the initially extracted zip url to get to the actual archive.
        :return:
        '''
        self.r = requests.get(url)
        self.url = url
        self.baseurl = url
        if baseurl:
            print("baseurl is not None")
            self.baseurl = baseurl


    def get_page_content(self, parser='html.parser', tagname='a', extpattern='\.zip$'):
        content = bs(self.r.text, parser)
        tag = content.find_all(tagname)
        pat = re.compile(extpattern)
        url_list = []
        failed = []

        for j in tag:
            path = j.attrs['href']

            if pat.search(path):
                url_list.append(self.baseurl + path)
            else:
                failed.append(path)
        for k in enumerate(failed, start=1):
            print(k)

        return(url_list)
