import re
from core.spider import Spider
from core.request import Request


class MaoProcess(object):

    def __init__(self) -> None:
        self.pattern = re.compile('<p class="name">[\s\S]*?title="([\s\S]*?)"')

    def process(self, page):
        html = page.content
        findall = self.pattern.findall(html)
        page.pageItems = findall


if __name__ == '__main__':
    spider = Spider(MaoProcess())
    rq = Request()
    rq.url = "https://maoyan.com/board/4"
    rq.headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    spider.request = rq
    spider.start()
