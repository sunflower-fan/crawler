import requests
from core.page import Page


class DefaultDownloader(object):

    def __init__(self) -> None:
        super().__init__()

    def download(self, request):
        rs = requests.get(url=request.url, headers=request.headers)
        page = Page()
        page.content = rs.text
        return page
