import re
from core.spider import Spider
from core.request import Request

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

base_url = "https://maoyan.com"


def get_detail_url(page):
    pattern = re.compile('<p class="name">[\s\S]*?href="([\s\S]*?)"')
    html = page.content
    new_requests = [Request(url=base_url + detail_url, processor=get_movie_info, headers=headers) for detail_url in
                    pattern.findall(html)]
    page.newRequests = new_requests


def get_movie_info(page):
    pattern = re.compile(
        '<div class="movie-brief-container" >[\s\S]*?class="name">([\s\S]*?)</h3>[\s\S]*?class="ellipsis">([\s\S]*?)</li>[\s\S]*?class="ellipsis">([\s\S]*?)</li>[\s\S]*?class="ellipsis">([\s\S]*?)</li>[\s\S]*?class="action-buyBtn"')
    info_list = pattern.findall(page.content)
    page.pageItems = [Item(name=info_list[0][0], country=info_list[0][2].replace('\n', ""), date=info_list[0][3])]


class Item(object):

    def __init__(self, name, country, date) -> None:
        self.name = name
        self.country = country
        self.date = date

    def __str__(self) -> str:
        return "name:{}, country:{}, date:{}".format(self.name, self.country, self.date)


if __name__ == '__main__':
    url = "https://maoyan.com/board/4?offset={}"
    rq = [Request(url=url.format(offset), processor=get_detail_url, headers=headers) for offset in range(0, 100, 10)]
    # rq = [Request(url=url.format(0), processor=get_detail_url, headers=headers)]
    spider = Spider(rq)
    spider.coro_num = 10
    spider.start()
    print("Elapsed time: {}".format(spider.t1 - spider.t0))
