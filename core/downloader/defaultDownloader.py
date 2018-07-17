from core.page import Page

import aiohttp


class DefaultDownloader(object):

    def __init__(self) -> None:
        super().__init__()

    async def download(self, rq, spider):
        if rq.url in spider.seen_url:
            return None
        async with aiohttp.request(method='GET', url=rq.url, headers=rq.headers) as r:
            content = await r.text()
            page = Page()
            page.http_status = r.status
            page.content = content
            spider.seen_url.add(rq.url)
            return page
