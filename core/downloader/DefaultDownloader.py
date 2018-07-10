import requests
from core import Page


class DefaultDownloader(object):

    def download(self, request):
        rs = requests.get(url=request.url, header=request.header)
        page = Page()
        page.content = rs.text
        return page
